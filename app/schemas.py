from pydantic import BaseModel, validator

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
        raise ValueError("Latitude must be between -180 and 180")
    return value

class AddressBaseSchema(BaseModel):
    id : str | None = None
    address : str
    latitude : float
    longitude : float

    # Validation for latitude:
    _check_latitude = validator("latitude")(validate_latitude)
    _check_longitude = validator("longitude")(validate_longitude)

    class Config:
        orm_mode = True # map the models to ORM object
        allow_population_by_field_name = True
        arbitrary_types_allowed = True