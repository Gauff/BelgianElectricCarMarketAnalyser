import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from src import file_management, utilities, data_cleaning
from src.data.electric_car_data import ElectricCar
import random
import time
from src.config import AUTOSCOUT24_RESULTS
from src.logging_config import setup_logging

# Set up logging
logger = setup_logging(__name__)

site_root_url = "https://www.autoscout24.be"
request_url = (f'{site_root_url}/fr/lst?atype=C&cy=B&damaged_listing=exclude&desc=0'
               f'&eq=110%2C49%2C37&fuel=E&offer=D%2CJ%2CU%2CN&powertype=kw'
               f'&pricefrom=500&priceto=400000&search_id=rtnyyq2l2h&sort=price'
               f'&source=listpage_pagination&ustate=N%2CU')
request_url_page = "&page="
file_name = 'autoscout24'


def get_cars_from_web_site():
    """
    Scrape car listings from AutoScout24 website.
    Returns list of ElectricCar objects.
    """
    page = 1
    all_cars = []
    consecutive_errors = 0
    max_consecutive_errors = 3

    logger.info("Starting AutoScout24 data scraping")

    while True:
        try:
            logger.info(f"AutoScout24: scraping page {page}")
            json_cars = _scrape_page(page)

            if not json_cars:  # Handle empty result
                logger.warning(f"No data found on page {page}")
                consecutive_errors += 1
                if consecutive_errors >= max_consecutive_errors:
                    logger.error(f"Max consecutive errors ({max_consecutive_errors}) reached. Stopping.")
                    break
                continue

            cars = [json.loads(x) for x in json.loads(json_cars)]

            if len(cars) == 0:
                logger.info("No more cars found. Finishing scraping.")
                break

            all_cars.extend(cars)
            consecutive_errors = 0  # Reset error counter on success
            _wait()
            page += 1

        except Exception as e:
            logger.error(f"Error while scraping page {page}: {str(e)}", exc_info=True)
            consecutive_errors += 1
            if consecutive_errors >= max_consecutive_errors:
                logger.error(f"Max consecutive errors ({max_consecutive_errors}) reached. Stopping.")
                break

    logger.info(f"Scraping completed. Found {len(all_cars)} cars")
    return _save_and_return(all_cars)


def get_cars_from_last_file():
    """
    Load car listings from the most recent JSON file.
    Returns list of ElectricCar objects.
    """
    try:
        json_file_path = file_management.get_last_generated_file_path(
            AUTOSCOUT24_RESULTS,
            file_name,
            '.json')

        if json_file_path is None:
            logger.info("No existing file found, fetching from website")
            return get_cars_from_web_site()

        logger.info(f"Loading cars from file: {json_file_path}")
        return _get_car_list_from_json_file(json_file_path)

    except Exception as e:
        logger.error(f"Error getting cars from last file: {str(e)}", exc_info=True)
        return []


def _create_driver():
    """
    Create and configure Chrome WebDriver instance.
    Returns configured WebDriver object.
    """
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Block image loading to improve performance
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            'profile.default_content_setting_values': {
                'cookies': 1, 'images': 2, 'javascript': 1,
                'plugins': 2, 'popups': 2, 'geolocation': 2,
                'notifications': 2, 'auto_select_certificate': 2,
                'fullscreen': 2, 'mouselock': 2, 'mixed_script': 2,
                'media_stream': 2, 'media_stream_mic': 2, 'media_stream_camera': 2,
                'protocol_handlers': 2, 'ppapi_broker': 2, 'automatic_downloads': 2,
                'midi_sysex': 2, 'push_messaging': 2, 'ssl_cert_decisions': 2,
                'metro_switch_to_desktop': 2, 'protected_media_identifier': 2,
                'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2
            }
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # Use ChromeDriverManager to handle driver installation
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("Chrome WebDriver created successfully")
        return driver

    except Exception as e:
        logger.error(f"Error creating Chrome driver: {str(e)}", exc_info=True)
        raise


def _scrape_page(page):
    """
    Scrape a single page of car listings.
    Returns JSON string containing car data.
    """
    driver = None
    try:
        driver = _create_driver()
        url = f'{request_url}{request_url_page}{page}' if page > 1 else request_url

        logger.info(f"Fetching URL: {url}")
        driver.get(url)
        time.sleep(2)  # Allow time for JavaScript to execute

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        json_data = _extract_json_from_html(soup)

        if not json_data:
            logger.warning("No valid JSON data found in the page source")
            return None

        listings_json_data = json_data["props"]["pageProps"]["listings"]
        cars = _get_car_list_from_json(listings_json_data)

        if not cars:
            logger.info("No cars found on this page")
            return json.dumps([])

        return json.dumps([car.to_json() for car in cars])

    except WebDriverException as e:
        logger.error(f"WebDriver error while scraping page {page}: {str(e)}", exc_info=True)
        return None
    except Exception as e:
        logger.error(f"Error while scraping page {page}: {str(e)}", exc_info=True)
        return None
    finally:
        if driver:
            try:
                driver.quit()
                logger.debug("WebDriver closed successfully")
            except Exception as e:
                logger.error(f"Error closing WebDriver: {str(e)}", exc_info=True)


def _extract_json_from_html(soup):
    """
    Extract JSON data from HTML.
    Returns JSON object or None if not found.
    """
    script_tags = soup.find_all('script')
    for script_tag in script_tags:
        if 'application/json' in script_tag.get('type', ''):
            try:
                json_data = json.loads(script_tag.string)
                if _validate_json_structure(json_data):
                    return json_data
            except json.JSONDecodeError:
                continue
    return None


def _validate_json_structure(json_data):
    """
    Validate the structure of the JSON data.
    Returns boolean indicating if structure is valid.
    """
    return (json_data
            and "props" in json_data
            and "pageProps" in json_data["props"]
            and "listings" in json_data["props"]["pageProps"])


def _get_car_list_from_json(listing_json_data):
    """
    Convert JSON listing data to ElectricCar objects.
    Returns list of ElectricCar objects.
    """
    cars = []
    for result in listing_json_data:
        try:
            car = ElectricCar(
                id=result['id'],
                brand_name=result["vehicle"]["make"].upper() if result["vehicle"]["make"] else "UNKNOWN",
                model_name=result["vehicle"]["model"].upper() if result["vehicle"]["model"] else "UNKNOWN",
                version=result["vehicle"]["modelVersionInput"].upper() if result["vehicle"][
                    "modelVersionInput"] else "UNKNOWN",
                body_style=result["vehicle"]["articleType"],
                vehicle_type="",
                published_date="",
                is_pro=False if result["seller"]["type"] == 'PrivateSeller' else True,
                new=False if result["vehicle"]['offerType'] == 'U' else True,
                first_registration_year=utilities.extract_year(result["tracking"]["firstRegistration"]),
                kilometers=result["tracking"]["mileage"],
                price=float(result["tracking"]["price"]),
                warranty_months=0,
                car_pass=False,
                description=', '.join([x['data'] for x in list(result["vehicleDetails"])]),
                url=_strip_after_jpg(f'{site_root_url}{result["url"]}'),
                point_of_sale_city=result["location"]["city"],
                image_url=_strip_after_jpg(result["images"][0] if result["images"] else None)
            )
            cars.append(car)

        except Exception as e:
            logger.error(f"Error processing car data: {str(e)}", exc_info=True)
            continue

    return cars


def _save_and_return(all_cars):
    """
    Save cars to JSON file and return the list.
    Returns list of ElectricCar objects.
    """
    if not all_cars:
        logger.warning("No cars to save")
        return []

    try:
        all_cars_json = json.dumps(all_cars)
        json_file_path = file_management.save_json(
            all_cars_json,
            AUTOSCOUT24_RESULTS,
            file_name,
            '.json')

        logger.info(f"Saved {len(all_cars)} cars to {json_file_path}")
        return _get_car_list_from_json_file(json_file_path)

    except Exception as e:
        logger.error(f"Error saving cars: {str(e)}", exc_info=True)
        return []


def _wait():
    """Add random delay between requests."""
    random_duration = random.uniform(3, 9)
    time.sleep(random_duration)


def _strip_after_jpg(url):
    """Strip URL after .jpg extension."""
    if url is None:
        return None

    jpg_index = url.find('.jpg')
    if jpg_index != -1:
        return url[:jpg_index + 4]
    return url


def _get_car_list_from_json_file(json_file_path):
    """
    Load cars from JSON file.
    Returns list of ElectricCar objects.
    """
    try:
        json_data = file_management.load_json(json_file_path)
        cars = []

        # json_data is already parsed by file_management.load_json()
        # No need to call json.loads() again
        for result in json_data:
            car = ElectricCar.from_json(json.dumps(result))
            cars.append(car)
        logger.info(f"Loaded {len(cars)} cars from file")
        return cars

    except Exception as e:
        logger.error(f"Error loading cars from JSON file: {str(e)}", exc_info=True)
        return []


if __name__ == '__main__':
    cars = get_cars_from_web_site()