import pandas as pd


def create_dataframe(electric_cars):
    # Create lists for each attribute of ElectricCar
    ids = [car.id for car in electric_cars]
    brand_names = [car.brand_name for car in electric_cars]
    model_names = [car.model_name for car in electric_cars]
    versions = [car.version for car in electric_cars]
    body_styles = [car.body_style for car in electric_cars]
    vehicle_types = [car.vehicle_type for car in electric_cars]
    published_dates = [car.published_date for car in electric_cars]
    is_pros = [car.is_pro for car in electric_cars]
    news = [car.new for car in electric_cars]
    first_registration_years = [car.first_registration_year for car in electric_cars]
    kilometers = [car.kilometers for car in electric_cars]
    prices = [car.price for car in electric_cars]
    warranty_months = [car.warranty_months for car in electric_cars]
    car_passes = [car.car_pass for car in electric_cars]
    descriptions = [car.description for car in electric_cars]
    urls = [car.url for car in electric_cars]
    point_of_sale_cities = [car.point_of_sale_city for car in electric_cars]
    image_urls = [car.image_url for car in electric_cars]

    # Create dictionary for DataFrame construction
    data = {
        "Id": ids,
        "Brand Name": brand_names,
        "Model Name": model_names,
        "Version": versions,
        "Body Style": body_styles,
        "Vehicle Type": vehicle_types,
        "Published Date": published_dates,
        "Is Pro": is_pros,
        "New": news,
        "First Registration Year": first_registration_years,
        "Kilometers": kilometers,
        "Price": prices,
        "Warranty Months": warranty_months,
        "Car Pass": car_passes,
        "Description": descriptions,
        "URL": urls,
        "Point of Sale City": point_of_sale_cities,
        "Image URL": image_urls,
    }

    # Create DataFrame
    df = pd.DataFrame(data)
    return df


def detect_price_drops(df_day1, df_day2):
    """
    Compares two dataframes containing ads from different days and detects the rows where the price has dropped.

    Args:
    df_day1 (pd.DataFrame): DataFrame containing 'Id' and 'Price' for day 1.
    df_day2 (pd.DataFrame): DataFrame containing 'Id' and 'Price' for day 2.

    Returns:
    pd.DataFrame: DataFrame containing 'Id', 'Price_day1', 'Price_day2', and 'Price_Drop'.
    """

    # Renaming the columns to avoid confusion after merging
    df_day1 = df_day1.rename(columns={"Price": "Price_day1"})
    df_day2 = df_day2.rename(columns={"Price": "Price_day2"})

    # Merging the dataframes on 'Id'
    merged_df = pd.merge(df_day1, df_day2, on="Id", how="inner")

    # Calculating the price drop
    merged_df["Price_Drop"] = merged_df["Price_day1"] - merged_df["Price_day2"]

    # Filtering the rows where the price has dropped
    price_drop_df = merged_df[merged_df["Price_Drop"] > 0]

    # Selecting relevant columns
    result_df = price_drop_df[["Id", "Price_day1", "Price_day2", "Price_Drop"]]

    return result_df
