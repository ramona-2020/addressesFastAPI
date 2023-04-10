import logging

from app import models

from app.database import get_db

from app.schemas import AddressBase

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException

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

@router.get('/address_id')
async def get_address(address_id: str, db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No address with this id: {address_id} found')
    return db_address

# Response will be a LIST of Address
@router.get('/addresses')
async def get_addresses(db: Session = Depends(get_db)):
    query = db.query(models.Address)
    addresses = query.all()
    logger.info('Getting addresses from database... [SUCCESS].')
    return addresses

@router.post('/')
async def create_address(address: AddressBase,
                         db: Session = Depends(get_db)):
    """
    Create data - used to create a new address
    :param address:
    :param db:
    :return: JSON representation
    """
    new_address = models.Address(address=address.address,
                                 latitude=address.latitude,
                                 longitude=address.longitude)

    # Generate a dictionary representation of the model, optionally specifying which fields to include or
    # exclude
    # add it to the session and commit it

    db.add(new_address) # that instance object to your database session.
    db.commit() # the changes to the database (so that they are saved)

    # update the patient instance to get the newly created Id
    db.refresh(new_address)

    logger.info('Created addresses... [SUCCESS].')
    return new_address

@router.put('/address_id')
async def update_address(address_id: str,
                         address: AddressBase,
                         db: Session = Depends(get_db)):
    note_query = db.query(models.Address).filter(models.Address.id == address_id)
    db_note = note_query.first()

    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {address_id} found')
    update_data = address.dict(exclude_unset=True)
    note_query.filter(models.Address.id == address_id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_note)
    return {"status": "success", "address": db_note}

@router.delete('/{address_id}')
async def delete_address(address_id: str,
                         db: Session = Depends(get_db)):
    db_address = db.query(models.Address).get(address_id)
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
    db_addresses = session.query(models.Address).all()

    addresses_within_distance = []
    for address in db_addresses:
        distance_address = haversine(latitude, longitude, address.latitude, address.longitude)
        if distance_address <= distance:
            addresses_within_distance.append(address)
    logger.info('Getting addresses within given distance ... [SUCCESS].')
    return {"status": "Addresses within given distance",
            'results': len(addresses_within_distance),
            'addresses': addresses_within_distance}
