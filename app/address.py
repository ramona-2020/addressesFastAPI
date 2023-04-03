import logging

from app import models, schemas

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

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


@router.get('/addresses')
async def get_addresses(session: Session = Depends(get_db)):
    addresses = session.query(models.Address).all()
    logger.info('Getting addresses from database... [SUCCESS].')
    return {'status': 'success', 'results': len(addresses), 'addresses': addresses}

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_address(payload: schemas.AddressBaseSchema, session: Session = Depends(get_db)):
    new_address = models.Address(**payload.dict())
    session.add(new_address)
    session.commit()
    session.refresh(new_address)
    logger.info('Created addresses... [SUCCESS].')
    return {"status": "success", "Address": new_address}

@router.patch('/{addressId}')
async def update_address(addressId: str, payload: schemas.AddressBaseSchema, session: Session = Depends(get_db)):
    address_query = session.query(models.Address).filter(models.Address.id == addressId)
    db_address = address_query.first()

    if not db_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No address with this id: {addressId} found')
    db_address = payload.dict(exclude_unset=True)
    for key, value in db_address.items():
        setattr(db_address, key, value)

    session.add(db_address)
    session.commit()
    session.refresh(db_address)
    logger.info(f'Updated addresses with {addressId}...[SUCCESS].')
    return {"status": "success", "address": db_address}

@router.delete('/{addressID}')
async def delete_address(addressId: str, session: Session = Depends(get_db)):
    db_address = session.query(models.Address).get(addressId)
    if not db_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No address with this id: {addressId} found')
    session.delete(db_address)
    session.commit()
    logger.info(f'Deleted addresses with {addressId}...[SUCCESS].')
    return {"status": "success"}

@router.get('/find/{latitude}/{longitude}/{distance}')
async def get_addresses_within_distance(latitude: float, longitude: float, distance: float, session: Session = Depends(get_db)):
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


