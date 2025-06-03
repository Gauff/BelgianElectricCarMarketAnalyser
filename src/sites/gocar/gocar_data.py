from dataclasses import dataclass

# Define data classes to represent the JSON structure
@dataclass
class Price:
    hasDiscount: bool = None
    original_price_gross: str = None
    percent: int = None
    unformatted: float = None
    for_filtering: int = None
    professional_price: int = None
    vat: int = None
    price_excl_tax: int = None
    vat_deductible: int = None
    to_bid: int = None
    formatted: str = None
    unformatted_reject_null_to_the_end: float = None

@dataclass
class Geo:
    lat: float = None
    lng: float = None

@dataclass
class Formatted:
    model_name: str = None
    l_bmarque: str = None
    l_model: str = None
    model_text: str = None
    version: str = None
    point_of_sale_name: str = None
    brand_name: str = None
    vehicle_options_list: list = None
    body_style: str = None
    gearbox: str = None
    fuel_type: str = None
    transmission: str = None
    pollution_class: str = None
    main_color: str = None
    first_registration_year: int = None
    point_of_sale_city: str = None
    description: str = None
    slug: str = None
    id: int = None
    vehicle_id: int = None
    cover: str = None
    published_at: str = None
    published_date: str = None
    l_id_marque: int = None
    l_id_modele: int = None
    l_b_version: str = None
    is_pro: int = None
    vehicle_type: str = None
    discount: int = None
    price: Price = None
    new: bool = None
    first_registration_label: str = None
    warranty_months: int = None
    weight: int = None
    kilometers: int = None
    images_count: int = None
    condition: str = None
    has_phyron_video: bool = None
    has_carpass_check: bool = None
    pollution_class_id: str = None
    number_of_doors: int = None
    number_of_seats: int = None
    smoke_filter: bool = None
    horse_power: int = None
    fiscal_horse_power: str = None
    engine_power_kw: int = None
    upsell_best_of: int = None
    upsell_top_result: int = None
    upsell_color: int = None
    upsell_facebook: int = None
    crashed: bool = None
    CO2_emissions: int = None
    brand_id: int = None
    brand_slug: str = None
    model_id: int = None
    point_of_sale_master: int = None
    url: str = None
    point_of_sale_id: int = None
    point_of_sale_address: str = None
    point_of_sale_zip: str = None
    _geo: Geo = None
    last_sync_timestamp: int = None
    point_of_sale_type: str = None
    point_of_sale_logo: str = None
    search_result_weight: int = None
    last_modified_timestamp: int = None
    point_of_sale_pro_first: int = None
    point_of_sale_pro_first_valid: int = None
    fuel_type_category: str = None
    is_leasing: bool = None
    model_slug: str = None
    model_all_names: str = None
