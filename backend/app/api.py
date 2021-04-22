from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from . import greyscale, applications

from . import crud, models, schemas
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def root() -> dict:
    return {"message": "Hello world!"}


@app.get("/set_greyscale_on")
async def set_greyscale_on() -> dict:
    greyscale.set_greyscale_on()
    return {"message": "Activated Greyscale Filter."}


@app.get("/set_greyscale_off")
async def set_greyscale_off() -> dict:
    greyscale.set_greyscale_off()
    return {"message": "Deactivated Greyscale Filter."}


@app.get("/running_processes")
async def get_running_processes() ->dict:
    return applications.get_process_list()


@app.get("/block_sets/", response_model=List[schemas.BlockSet])
def get_block_sets(db: Session = Depends(get_db)):
    return crud.get_block_sets(db)


@app.get("/block_sets/{block_set_id}")
def get_block_set(block_set_id: int, db: Session = Depends(get_db)):
    block_set = crud.get_block_set(db, block_set_id)
    if block_set is None:
        raise HTTPException(status_code=404, detail="Block Set not found")
    return block_set


@app.get("/block_sets/{block_set_id}/applications")
def get_block_set(block_set_id: int, db: Session = Depends(get_db)):
    block_set = crud.get_block_set(db, block_set_id)
    if block_set is None:
        raise HTTPException(status_code=404, detail="Block Set not found")

    apps = crud.get_applications_by_block_set(db, block_set_id)

    if apps is None:
        raise HTTPException(status_code=404, detail="Block Set not found or ")
    return block_set


@app.get("/block_sets/{block_set_id}/{application_path}/block/")
def block_application(block_set_id: int, application_path: str, db: Session = Depends(get_db)):

    crud.create_application(db=db, )


