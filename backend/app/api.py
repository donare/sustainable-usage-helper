from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from . import greyscale, applications

from sqlalchemy.ext.asyncio import AsyncSession
from .db import schemas, service
from .db.models.blockset import BlockSet
from app.db.config import engine, get_db

from typing import List

app = FastAPI()

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


@app.on_event("startup")
async def startup():
    await service.recreate_tables()
    await service.create_defaults()


@app.on_event("shutdown")
async def shutdown():
    pass


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


@app.get("/block_sets/", response_model=List[schemas.BlockSet])  # todo: fixen, dass beim service tatsächlich das Schema herauskommt!
async def get_block_sets(db_session: AsyncSession = Depends(get_db)):
    return await BlockSet.find_all(db_session)


@app.get("/block_sets/{block_set_id}")
async def get_block_set(block_set_id: int, db_session: AsyncSession = Depends(get_db)):
    return await BlockSet.find_by_id(db_session, block_set_id)


@app.get("/block_sets/{block_set_id}/applications")
async def get_block_set(block_set_id: int, db_session: AsyncSession = Depends(get_db)):
    return await BlockSet.get_applications(db_session, block_set_id)


@app.get("/block_sets/{block_set_id}/{application_path}/block/")
async def block_application(block_set_id: int, application_path: str, db_session: AsyncSession = Depends(get_db)):
    pass
    # crud.create_application(db=db, )


