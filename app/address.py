import logging
from typing import List

from sqlalchemy.orm import Session

from app import models
from app.schemas import AddressBaseSchema as Address
from app.schemas import CreateAddressRequest

from fastapi import APIRouter, Depends, status, HTTPException

from app.database import get_db
from math import radians, sin, cos, sqrt, atan2

# init our logger
logger = logging.getLogger("simple_example")

router = APIRouter()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    return distance

# CRUD Routes

@router.get('/address_id', response_model=Address)
async def get_address(address_id: str, db: Session):
    address = db.query(Address).filter(Address.id == address_id).first()
    return address

# Response will be a LIST of Address
@router.get('/addresses', response_model=List[Address])
async def get_addresses(db: Session = Depends(get_db)):
    addresses = db.query(Address).all()
    logger.info('Getting addresses from database... [SUCCESS].')
    return addresses

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_address(request: CreateAddressRequest,
                         db: Session = Depends(get_db)):
    """
    Create data - used to create a new address
    :param request:
    :param db:
    :return: JSON representation
    """
    new_address = Address(**request.dict())
    db.add(new_address) # that instance object to your database session.
    db.commit() # the changes to the database (so that they are saved)
    db.refresh(new_address) # your instance (so that it contains any new data from the database, like the generated ID).
    logger.info('Created addresses... [SUCCESS].')
    return new_address

@router.patch('/address_id', response_model=Address)
async def update_address(address_id: str,
                         db: Session = Depends(get_db)):
    address = db.query(Address).filter(models.Address.id == address_id).first()
    return address

@router.delete('/{address_id}')
async def delete_address(address_id: str,
                         db: Session = Depends(get_db)):
    db_address = db.query(Address).get(address_id)
    if not db_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No address with this id: {address_id} found')
    db.delete(db_address)
    db.commit()
    logger.info(f'Deleted addresses with {address_id}...[SUCCESS].')
    return {"status": "success"}


@router.get('/find/{latitude}/{longitude}/{distance}')
async def get_addresses_within_distance(latitude: float,
                                        longitude: float,
                                        distance: float,
                                        session: Session = Depends(get_db)):
    db_addresses = session.query(CreateAddressRequest).all()

    addresses_within_distance = []
    for address in db_addresses:
        distance_address = haversine(latitude, longitude, address.latitude, address.longitude)
        if distance_address <= distance:
            addresses_within_distance.append(address)
    logger.info('Getting addresses within given distance ... [SUCCESS].')
    return {"status": "Addresses within given distance",
            'results': len(addresses_within_distance),
            'addresses': addresses_within_distance}

