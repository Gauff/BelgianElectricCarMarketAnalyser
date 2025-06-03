import json
from dataclasses import dataclass


@dataclass
class ElectricCar:
    id: str

    brand_name: str
    model_name: str
    version: str

    body_style: str
    vehicle_type: str

    published_date: str
    is_pro: int
    new: bool
    first_registration_year: int
    kilometers: int

    price: float
    warranty_months: int
    car_pass: bool

    description: str

    url: str
    image_url: str
    point_of_sale_city: str

    def to_json(self):
        return json.dumps(self.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)
