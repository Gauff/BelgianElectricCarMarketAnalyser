from dataclasses import dataclass
from typing import List


@dataclass
class Listing:
    id: str
    evBanner: dict
    images: List[str]
    ocsImagesA: List[str]
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
    specialConditions: List[str]
    statistics: dict
    searchResultType: str
    tracking: dict
    coverImageAttractiveness: float
    vehicleDetails: List[dict]
    isAmmListing: bool
