def get_sort_key(brand_name, model_name):
    # Return a tuple of brand_name and model_name for sorting
    return f"{brand_name.upper()} {model_name.upper()}"


def get_registration_year(car):
    # Return 0 if first_registration_year is None, otherwise return the integer value
    return (
        int(car.first_registration_year)
        if car.first_registration_year is not None
        else 0
    )
