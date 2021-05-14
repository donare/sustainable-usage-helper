from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware

from . import greyscale, applications

from sqlalchemy.ext.asyncio import AsyncSession
from .db import schemas, service
from .db.models.blockset import BlockSet
from .db.models.application import Application
from .db.models.timeframe import TimeFrame
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


@app.get("/block_sets/", response_model=List[schemas.BlockSet])
async def get_block_sets(db_session: AsyncSession = Depends(get_db)):
    return await BlockSet.find_all(db_session)


@app.post("/block_sets/", response_model=schemas.BlockSet)
async def add_block_set(block_set: schemas.BlockSetCreate, db_session: AsyncSession = Depends(get_db)):
    new_block_set = BlockSet(block_set)
    return await new_block_set.add_self(db_session)


@app.get("/block_sets/{block_set_id}/delete", status_code=status.HTTP_200_OK)
async def remove_block_set(block_set_id: int, db_session: AsyncSession = Depends(get_db)):
    block_set = await BlockSet.find_by_id(block_set_id, db_session)
    await block_set.delete_self(db_session)


@app.get("/block_sets/{block_set_id}", response_model=schemas.BlockSet)
async def get_block_set(block_set_id: int, db_session: AsyncSession = Depends(get_db)):
    return await BlockSet.find_by_id(block_set_id, db_session)


@app.get("/block_sets/{block_set_id}/applications", response_model=List[schemas.Application])
async def get_blocked_applications(block_set_id: int, db_session: AsyncSession = Depends(get_db)):
    return await BlockSet.get_applications(block_set_id, db_session)


@app.post("/block_sets/{block_set_id}/block/", response_model=schemas.BlockSet, status_code=status.HTTP_200_OK)
async def block_applications(block_set_id: int, applications: List[schemas.ApplicationCreate], db_session: AsyncSession = Depends(get_db)):
    for a in applications:
        new_app = Application(a)

        db_app = await new_app.add_self(db_session)

        await BlockSet.block_application(block_set_id, db_app, db_session)

    return await BlockSet.find_by_id(block_set_id, db_session)


@app.post("/block_sets/{block_set_id}/unblock/", response_model=schemas.BlockSet, status_code=status.HTTP_200_OK)
async def unblock_applications(block_set_id: int, applications: List[schemas.ApplicationCreate], db_session: AsyncSession = Depends(get_db)):
    for a in applications:
        db_app = await Application.find_by_path(a.app_path, db_session)

        await BlockSet.unblock_application(block_set_id, db_app, db_session)

    return await BlockSet.find_by_id(block_set_id, db_session)


@app.post("/block_sets/{block_set_id}/add_timeframes")
async def add_timeframes_to_block_set(block_set_id: int, timeframes: List[schemas.TimeFrameCreate], db_session: AsyncSession = Depends(get_db)):
    for t in timeframes:
        new_timeframe = TimeFrame(t)
        db_timeframe = await new_timeframe.add_self(db_session)

        await BlockSet.add_time_frame(block_set_id, db_timeframe, db_session)

    return await BlockSet.find_by_id(block_set_id, db_session)


@app.post("/block_sets/{block_set_id}/remove_timeframes")
async def remove_timeframes_from_block_set(block_set_id: int, timeframes: List[schemas.TimeFrame], db_session: AsyncSession = Depends(get_db)):
    for t in timeframes:
        db_timeframe = await TimeFrame.find_by_id(t.id, db_session)

        await BlockSet.remove_time_frame(block_set_id, db_timeframe, db_session)

    return await BlockSet.find_by_id(block_set_id, db_session)
