from typing import Optional

from pydantic import BaseModel, validator, Field


def validate_latitude(value: float) -> float:
    """
    Latitude must be a number between -90 and 90
    :param value:
    :return: value
    """
    if not -90 <= abs(value) <= 90:
        raise ValueError("Latitude must be between -90 and 90")
    return value

def validate_longitude(value: float) -> float:
    """
    Longitude must a number between -180 and 180
    :param value:
    :return:
    """
    if not -180 <= abs(value) <= 180:
        raise ValueError("Longitude must be between -180 and 180")
    return value


class CreateAddress(BaseModel):
    id: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class AddressBase(BaseModel):
    id: Optional[str]= None
    address : str = Field(min_length=10, max_length=255)
    latitude : float
    longitude : float

    # Validation for latitude and longitude:
    _check_latitude = validator("latitude")(validate_latitude)
    _check_longitude = validator("longitude")(validate_longitude)

    # provide configurations to Pydantic
    class Config:
        orm_mode = True # map the ORM models to ORM object - tell the Pydantic model to read the data
                        # even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "address": "Address description",
                "latitude": "Address latitude",
                "longitude": "Address longitude",
            }
        }


