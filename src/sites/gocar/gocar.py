import os
from dotenv import load_dotenv
from src import file_management, utilities
from src.data.electric_car_data import ElectricCar
from src.sites import http_client
from src.sites.gocar.gocar_data import Formatted
from src.sites.search_settings import SearchSettings

# Load environment variables
load_dotenv()

# Get token from environment variables
bearer_token = os.getenv('GOCAR_BEARER_TOKEN')
if not bearer_token:
    raise ValueError("GOCAR_BEARER_TOKEN not found in environment variables. Please add it to your .env file.")

# Get cars from :
# - web site
# - last cached file

result_file_path = os.path.join('results', 'gocar')
file_name = 'gocar'
query_url = "https://search.gocar.be/multi-search"
request_json_file_path = os.path.join('src', 'sites', 'gocar', 'gocar_electric_car_search.json')

def get_cars_from_web_site():
    print(f"Gocar")
    json_data = _perform_http_request()
    json_file_path = file_management.save_json(
        json_data,
        result_file_path,
        file_name,
        '.json')
    car_list = _get_car_list_from_json(json_data)
    return car_list

def get_cars_from_last_file():
    json_file_path = file_management.get_last_generated_file_path(
        result_file_path,
        file_name,
        '.json')

    if json_file_path is None:
        return get_cars_from_web_site()
    else:
        return _get_car_list_from_json_file(json_file_path)

def _get_search_settings():
    settings = SearchSettings(
        query_url,
        bearer_token)
    settings.add_header("Content-Type", "application/json")
    settings.add_header("User-Agent", "MyApp/1.0")
    # Read JSON from file and update the body
    settings.set_body_from_json_file(request_json_file_path)
    return settings


def _get_search_settings():
    settings = SearchSettings(
        query_url,
        "5e8d520f3d3918d16f9a79b1b964977612c1b7f738d4530a078cfd8bcdc485bd")
    settings.add_header("Content-Type", "application/json")
    settings.add_header("User-Agent", "MyApp/1.0")
    # Read JSON from file and update the body
    settings.set_body_from_json_file(request_json_file_path)

    return settings


def _perform_http_request():
    gocar_search_settings = _get_search_settings()
    json_data = http_client.perform_post(gocar_search_settings)
    return json_data


def _get_car_list_from_json_file(json_file_path):
    json_data = file_management.load_json(json_file_path)

    return _get_car_list_from_json(json_data)


def _get_car_list_from_json(json_data):
    cars = []
    for result in json_data['results'][0].get('hits', []):
        formatted_data = Formatted(**result['_formatted'])

        p = formatted_data.price
        pr = float(p.get('for_filtering', p.get('unformatted', 0.0)))

        car = ElectricCar(
            id=formatted_data.id,
            brand_name=formatted_data.l_bmarque.upper(),
            model_name=formatted_data.l_model.upper(),
            version=formatted_data.l_b_version.upper(),
            body_style=formatted_data.body_style,
            vehicle_type=formatted_data.vehicle_type,
            published_date=formatted_data.published_date,
            is_pro=bool(formatted_data.is_pro),
            new=formatted_data.new,
            first_registration_year=utilities.extract_year(formatted_data.first_registration_year),
            kilometers=formatted_data.kilometers,
            price=pr,
            warranty_months=utilities.extract_int(formatted_data.warranty_months),
            car_pass=formatted_data.has_carpass_check,
            description=formatted_data.description,
            url=formatted_data.url,
            point_of_sale_city=formatted_data.point_of_sale_city,
            image_url=formatted_data.cover
        )

        cars.append(car)
    return cars


def _strip_after_jpg(url):
    if url is None:
        return None

    jpg_index = url.find('.jpg')
    if jpg_index != -1:
        return url[:jpg_index + 4]
    return url


if __name__ == '__main__':
    get_cars_from_web_site()