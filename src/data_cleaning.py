import src.data.electric_car_models


forbidden_list = [
    "ESSENCE", "BENZINE", "DIESEL", "PETROL", "CNG", "HYBRID", "HYBRIDE",
    "CYLINDRE", "CYLINDREE", "CC", "CM2",
    "0.9", "1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9", "2.0", "2.1", "2.2", "2.3"
    "TCE", "TFSI", "CRDI", "TDI", "TDCI", "VTVT", "SHVS", "D4D", "DTEC", "MULTIJET", "DCI", "7G-DCT", "TSI", "CDI", "VTECH", "GTI", "HDI",
    "118I", "318I", "420D", "428I", "520D", "530XD", "730D", "FIAT 695", "S TRONIC", "FOCUS", "180 D", "C 220", "TEKNA",
    "GOLF 1", "SCENIC", "MEGANE", "488 GTB", "S2000", "216D", "316", "430I", "525D", "M125I", "320CI", "330E", "435I", "530E", "520 M",
    "DOKKER", "220D", "M135I", "GTD", "TWINGO PHASE",
    "SOUPAPE", "BIELLE", "CULASSE",
    "TOY",
    "BRADSHAW", "LINDE",
    ]


def clean_car_list(cars):
    # Clean
    cars = [car for car in cars if
            not any(forbidden_term in car.description.upper() for forbidden_term in src.data_cleaning.forbidden_list)]
    filtered_cars = []
    for car in cars:
        description = f"{car.brand_name} {car.model_name} {car.description} {car.version}"
        make, model = src.data.electric_car_models.find_make_and_model(description)

        if make is None or model is None:
            continue

        car.brand_name = make
        car.model_name = model

        if car.first_registration_year not in [None, '0'] and int(car.first_registration_year) < 2000:
            car.first_registration_year = int(car.first_registration_year) + 100

        filtered_cars.extend([car])

    return filtered_cars