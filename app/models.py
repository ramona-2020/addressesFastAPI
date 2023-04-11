from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Float

Base = declarative_base()

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Address: {self.id}," \
               f"\n {self.address} " \
               f"at {self.latitude} | {self.longitude}>"