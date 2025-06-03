import concurrent.futures

import pandas

from src import data_cleaning, file_management
from src.config import RESULTS_DIR
from src.data import electric_car_models, dataframes
from src.logging_config import setup_logging
from src.sites.autoscout24 import autoscout24
from src.sites.deuxieme_main import deuxieme_main
from src.sites.gocar import gocar
from src.visualization import get_registration_year

# Set up logging
logger = setup_logging(__name__)

file_name = "df"


def get_cars(source="web"):
    """
    Get cars from all sources, either from web or file.
    If source is 'web', scrapes all sources in parallel.

    Args:
        source (str): Either 'web' or 'file'

    Returns:
        list: Combined list of ElectricCar objects from all sources
    """
    if source == "web":
        return _get_cars_parallel()
    elif source == "file":
        return _get_cars_from_files()
    else:
        raise ValueError("Invalid data source. Choose 'web' or 'file'.")


def _get_cars_parallel():
    """
    Scrape cars from all sources in parallel using ThreadPoolExecutor.

    Returns:
        list: Combined list of ElectricCar objects from all sources
    """
    all_cars = []
    scraping_functions = [
        ("Gocar", gocar.get_cars_from_web_site),
        ("AutoScout24", autoscout24.get_cars_from_web_site),
        ("2ememain", deuxieme_main.get_cars_from_web_site),
    ]

    logger.info("Starting parallel scraping from all sources")

    # Using ThreadPoolExecutor since our tasks are I/O bound
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all scraping tasks
        future_to_source = {
            executor.submit(func): name for name, func in scraping_functions
        }

        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_source):
            source_name = future_to_source[future]
            try:
                cars = future.result()
                logger.info(f"{source_name}: Found {len(cars)} cars")
                all_cars.extend(cars)
            except Exception as e:
                logger.error(f"Error scraping {source_name}: {e!s}", exc_info=True)

    logger.info(f"Parallel scraping completed. Total cars found: {len(all_cars)}")
    return all_cars


def _get_cars_from_files():
    """
    Load cars from the most recent files for all sources.

    Returns:
        list: Combined list of ElectricCar objects from all sources
    """
    cars = []
    try:
        logger.info("Loading cars from Gocar")
        cars.extend(gocar.get_cars_from_last_file())

        logger.info("Loading cars from AutoScout24")
        cars.extend(autoscout24.get_cars_from_last_file())

        logger.info("Loading cars from 2ememain")
        cars.extend(deuxieme_main.get_cars_from_last_file())

        logger.info(f"Loaded {len(cars)} cars from files")
    except Exception as e:
        logger.error(f"Error loading cars from files: {e!s}", exc_info=True)

    return cars


def filter_cars(cars, min_price=500, max_price=150000):
    """Filter cars by price range."""
    filtered = [car for car in cars if min_price <= car.price <= max_price]
    logger.info(
        f"Filtered {len(cars)} cars to {len(filtered)} within price range {min_price}-{max_price}"
    )
    return filtered


def split_description(description):
    """Split description into lines of maximum 100 characters."""
    if not isinstance(description, str):
        return description

    words = description.split()
    lines = []
    line_length = 0
    line = ""

    for word in words:
        if line_length + len(word) > 100:
            lines.append(line)
            line = ""
            line_length = 0
        line += word + " "
        line_length += len(word) + 1

    lines.append(line)
    return "<br>".join(lines)


def clean_car_list(cars):
    """Clean and validate car data."""
    logger.info(f"Starting cleaning of {len(cars)} cars")

    # Remove cars with forbidden terms
    cars = [
        car
        for car in cars
        if not any(
            forbidden_term in car.description.upper()
            for forbidden_term in data_cleaning.forbidden_list
        )
    ]

    logger.info(f"{len(cars)} cars remaining after forbidden term filtering")

    filtered_cars = []
    for car in cars:
        try:
            description = (
                f"{car.brand_name} {car.model_name} {car.description} {car.version}"
            )
            make, model = electric_car_models.find_make_and_model(description)

            if make is None or model is None:
                continue

            car.brand_name = make
            car.model_name = model

            if (
                car.first_registration_year is not None
                and car.first_registration_year != "0"
                and int(car.first_registration_year) < 2000
            ):
                car.first_registration_year = int(car.first_registration_year) + 100

            filtered_cars.append(car)

        except Exception as e:
            logger.error(f"Error cleaning car data: {e!s}", exc_info=True)
            continue

    logger.info(f"Cleaning completed. {len(filtered_cars)} cars remaining")
    return filtered_cars


def prepare_dataset_for_display(cars):
    """Prepare car data for visualization."""
    logger.info("Preparing dataset for display")

    try:
        model_names = [
            f"{car.brand_name.upper()} {car.model_name.upper()}".strip() for car in cars
        ]
        registration_years = [get_registration_year(car) for car in cars]

        df = dataframes.create_dataframe(cars)
        df["model"] = pandas.Series(model_names)
        df["year"] = pandas.Series(registration_years)
        df["desc"] = df["Description"].apply(split_description)

        df_sorted = df.sort_values(by=["year", "model"], ascending=[True, True])
        df_sorted.drop_duplicates(inplace=True)

        logger.info(f"Dataset prepared with {len(df_sorted)} unique entries")
        return df_sorted

    except Exception as e:
        logger.error(f"Error preparing dataset: {e!s}", exc_info=True)
        return pandas.DataFrame()


def save_dataframe(df):
    """Save DataFrame to pickle file."""
    try:
        file_path = file_management.save_pickle(df, RESULTS_DIR, file_name)
        logger.info(f"DataFrame saved to {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error saving DataFrame: {e!s}", exc_info=True)
        return None


def detect_price_drops():
    """Detect price drops between the last two scraped datasets."""
    try:
        file_paths = file_management.get_two_lasts_generated_file_path(
            RESULTS_DIR, file_name, ".pkl"
        )

        if not file_paths:
            logger.warning("No files found for price drop detection")
            return None, None

        if len(file_paths) == 1:
            logger.info("Only one file found, cannot detect price drops")
            return None, None

        logger.info("Loading DataFrames for price drop detection")
        df_day1 = file_management.load_pickle(file_paths[1])
        df_day2 = file_management.load_pickle(file_paths[0])

        df_drop = dataframes.detect_price_drops(df_day1, df_day2)

        if df_drop.empty:
            logger.info("No price drops detected")
            return None, None

        ids_with_price_drop = df_drop["Id"]
        df_day2_filtered = df_day2[df_day2["Id"].isin(ids_with_price_drop)]
        df_day2_filtered = pandas.merge(
            df_day2_filtered, df_drop[["Id", "Price_Drop"]], on="Id", how="inner"
        )

        logger.info(f"Detected {len(df_drop)} price drops")
        logger.info("\nPrice Drop Summary:")
        logger.info(df_day2_filtered.describe())

        return df_drop, df_day2_filtered

    except Exception as e:
        logger.error(f"Error detecting price drops: {e!s}", exc_info=True)
        return None, None
