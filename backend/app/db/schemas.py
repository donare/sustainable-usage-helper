from typing import List, Optional

from pydantic import BaseModel

from datetime import time


class ApplicationBase(BaseModel):
    app_path: str


class ApplicationCreate(ApplicationBase):
    pass


class Application(ApplicationBase):
    id: int

    class Config:
        orm_mode = True


class TimeFrameBase(BaseModel):
    start_time: time
    end_time: time
    weekdays: int


class TimeFrameCreate(TimeFrameBase):
    pass


class TimeFrame(TimeFrameBase):
    id: int
    block_set_id: int

    class Config:
        orm_mode = True


class BlockSetBase(BaseModel):
    name: str


class BlockSetCreate(BlockSetBase):
    pass


class BlockSet(BlockSetBase):
    id: int
    apps: List[Application] = []
    time_frames: List[TimeFrame] = []

    class Config:
        orm_mode = True
