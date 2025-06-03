from dataclasses import dataclass


@dataclass
class Listing:
    id: str
    evBanner: dict
    images: list[str]
    ocsImagesA: list[str]
    price: dict
    availableNow: bool
    superDeal: dict
    url: str
    vehicle: dict
    location: dict
    ratings: dict
    seller: dict
    appliedAdTier: str
    adTier: str
    isOcs: bool
    specialConditions: list[str]
    statistics: dict
    searchResultType: str
    tracking: dict
    coverImageAttractiveness: float
    vehicleDetails: list[dict]
    isAmmListing: bool
