#pro_search =         r'attributesById[]=10899&attributesById[]=10882&attributesById[]=11756&attributesByKey[]=Language:all-languages&l1CategoryId=91&searchInTitleAndDescription=true&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view'
#pro_search =         r'attributesById%5B%5D=10899&attributesById%5B%5D=10882&attributesById%5B%5D=11756&attributesByKey%5B%5D=Language%3Aall-languages&l1CategoryId=91&searchInTitleAndDescription=true&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view'
#particulier_search = r'attributesById%5B%5D=10882&attributesById%5B%5D=10898&attributesById%5B%5D=11756&attributesByKey%5B%5D=Language%3Aall-languages&l1CategoryId=91&searchInTitleAndDescription=true&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view'
#query_url_pro_search = f"{query_url}{pro_search}"
#query_url_particulier_search = f"{query_url}{particulier_search}"

"""
attributesById[]=10899
attributesById[]=10882
attributesById[]=11756
attributesByKey[]=Language%3Aall-languages
l1CategoryId=91
limit=30
offset=30
searchInTitleAndDescription=true
sortBy=SORT_INDEX
sortOrder=DECREASING
viewOptions=list-view
"""
import json
import requests
import random
import time
from src import file_management, utilities, data_cleaning
from src.data.electric_car_data import ElectricCar
from src.config import DEUXIEMEMAIN_RESULTS
from src.logging_config import setup_logging

# Set up logging
logger = setup_logging(__name__)

root_url = "https://www.2ememain.be"
query_url = f"{root_url}/lrp/api/search?"
search = r'attributesById%5B%5D=10882&attributesById%5B%5D=11756&attributesByKey%5B%5D=Language%3Aall-languages&l1CategoryId=91&searchInTitleAndDescription=true&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view'
items_per_page = 100
page_parameter = f"&limit={items_per_page}&offset="

query_url_search = f"{query_url}{search}"
file_name = 'deuxieme_main'


def get_cars_from_web_site():
    all_cars = []
    page = 1

    try:
        logger.info("Starting 2ememain data scraping")
        json_data = _perform_http_request(page)

        if not json_data:
            logger.warning("No data received from initial request")
            return []

        max_allowed_page_number = json_data.get('maxAllowedPageNumber')
        if not max_allowed_page_number:
            logger.error("Could not find maxAllowedPageNumber in response")
            return []

        listing_json_data = json_data.get("listings", [])
        cars = _get_car_list_from_json(listing_json_data)
        all_cars.extend(cars)

        logger.info(f"Found {max_allowed_page_number} pages to scrape")

        while page <= max_allowed_page_number:
            try:
                _wait()
                page += 1
                logger.info(f"2eme main: scraping page {page} / {max_allowed_page_number}")

                json_data = _perform_http_request(page)
                if not json_data:
                    continue

                listing_json_data = json_data.get("listings", [])
                cars = _get_car_list_from_json(listing_json_data)
                all_cars.extend(cars)

            except Exception as e:
                logger.error(f"Error processing page {page}: {str(e)}", exc_info=True)
                continue

        # Save results even if some pages failed
        return _save_and_return(all_cars)

    except Exception as e:
        logger.error(f"Error in get_cars_from_web_site: {str(e)}", exc_info=True)
        return _save_and_return(all_cars)


def get_cars_from_last_file():
    try:
        json_file_path = file_management.get_last_generated_file_path(
            DEUXIEMEMAIN_RESULTS,
            file_name,
            '.json')

        if json_file_path is None:
            logger.info("No existing file found, fetching from website")
            return get_cars_from_web_site()
        else:
            return _get_car_list_from_json_file(json_file_path)
    except Exception as e:
        logger.error(f"Error getting cars from last file: {str(e)}", exc_info=True)
        return []


def _get_page_parameter(page):
    offset = (page - 1) * items_per_page
    return f"{page_parameter}{offset}"


def _perform_http_request(page):
    try:
        url = f"{query_url_search}{_get_page_parameter(page)}"

        headers = {
            'Cookie': 'BNL20533_VISITED=true; route_65096237_fb4d_4561_b305_7b204b0db8cf=50cfb3a62c6dea7728413516252b97e7'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes

        return response.json()
    except requests.RequestException as e:
        logger.error(f"HTTP request failed for page {page}: {str(e)}", exc_info=True)
        return None


def _save_and_return(all_cars):
    if not all_cars:
        logger.warning("No cars to save")
        return []

    try:
        all_cars_json = json.dumps(list([car.__dict__ for car in all_cars]))
        json_file_path = file_management.save_json(
            all_cars_json,
            DEUXIEMEMAIN_RESULTS,
            file_name,
            '.json')

        return all_cars
    except Exception as e:
        logger.error(f"Error saving cars: {str(e)}", exc_info=True)
        return []


def _wait():
    random_duration = random.uniform(3, 9)
    time.sleep(random_duration)


def _get_car_list_from_json(listing_json_data):
    cars = []
    for data in listing_json_data:
        try:
            make = next((x for x in data["verticals"] if x not in ['cars', 'automotive']), None)
            year = next((d['value'] for d in data["attributes"] if d['key'] == "constructionYear"), None)

            car = ElectricCar(
                id=data['itemId'],
                brand_name=make.upper() if make is not None else "UNKNOWN",
                model_name=next((d['value'].upper() for d in data["attributes"] if d['key'] == "model"), data["title"]),
                version="UNKNOWN",
                body_style=next((d['value'].upper() for d in data["attributes"] if d['key'] == "body"), "UNKNOWN"),
                vehicle_type="",
                published_date=data["date"],
                is_pro=True,
                new=False,
                first_registration_year=year,
                kilometers=next((d['value'] for d in data["attributes"] if d['key'] == "mileage"), None),
                price=float(data["priceInfo"]["priceCents"] / 100),
                warranty_months=0,
                car_pass=False,
                description=_build_description(data),
                url=f'{root_url}{data["vipUrl"]}',
                point_of_sale_city=data["location"]["cityName"],
                image_url=_get_image_url(data)
            )

            if year is None:
                year = utilities.extract_year(car.description)
                if year is not None:
                    car.first_registration_year = int(year)

            if car.first_registration_year is not None and int(car.first_registration_year) < 2000:
                car.first_registration_year = int(car.first_registration_year) + 100

            forbidden = any(forbidden_term in car.description.upper()
                            for forbidden_term in data_cleaning.forbidden_list)

            if not forbidden:
                cars.append(car)

        except Exception as e:
            logger.error(f"Error processing car data: {str(e)}", exc_info=True)
            continue

    return cars


def _build_description(data):
    """Build complete description from all available data"""
    parts = [
        data["title"],
        data["description"],
        ', '.join(list(next((d['values'] for d in data["attributes"] if d['key'] == "options"), []))),
        ', '.join(list(next((d['values'] for d in data["extendedAttributes"]), [])))
    ]
    return " | ".join(filter(None, parts))


def _get_image_url(data):
    """Get first image URL if available"""
    if "imageUrls" in data and data["imageUrls"]:
        return "https://" + data["imageUrls"][0].replace('//', '')
    return None


def _get_car_list_from_json_file(json_file_path):
    try:
        json_data = file_management.load_json(json_file_path)

        # Handle cases where json_data might be a single string or invalid format
        if not isinstance(json_data, list):
            logger.error(f"JSON data is not a list: {type(json_data)}")
            return []

        cars = []
        for item in json_data:
            # Skip any non-dictionary items
            if not isinstance(item, dict):
                logger.warning(f"Skipping invalid car data: {item}")
                continue

            try:
                cars.append(ElectricCar(**item))
            except TypeError as e:
                logger.warning(f"Could not create ElectricCar from item {item}: {str(e)}")
                continue

        return cars

    except Exception as e:
        logger.error(f"Error loading cars from JSON file: {str(e)}", exc_info=True)
        return []


if __name__ == '__main__':
    car_list = get_cars_from_web_site()