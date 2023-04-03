from app import address, models, database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
FORMAT = "%(levelname)s:%(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

#  create the SQL table in the SQLite database
models.Base.metadata.create_all(bind=database.engine)

# create FastApi app
app = FastAPI()

# init our logger
log = logging.getLogger("simple_example")

# list of the allowed origins
origins = [
    "http://localhost:3000",
]

# configure the app to accept cross-origin domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add the router to the middleware stack
app.include_router(address.router, tags=['Addresses'], prefix='/api')


@app.get("/")
def root():
    return {"message": "Welcome to addressesAPI with SQLAlchemy"}
