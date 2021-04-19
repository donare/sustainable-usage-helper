from sqlalchemy.orm import Session

from .models import *
from datetime import datetime as dt


def get_application(db: Session, application_id: int):
    return db.query(Application)\
        .filter(Application.id == application_id).first()


def get_applications(db:Session):
    return db.query(Application)


def get_blocked_applications(db: Session):
    now = dt.now()
    time = now.time()
    weekday = now.weekday()
    weekday_mask = 1 << weekday

    return db.query(Application)\
        .join(Application.block_sets)\
        .join(BlockSet.time_frames)\
        .filter(TimeFrame.start_time >= time)\
        .filter(TimeFrame.end_time <= time)\
        .filter(TimeFrame.weekdays & weekday_mask)


def get_block_sets(db: Session):
    return db.query(BlockSet)


def get_block_set(db: Session, block_set_id: int):
    return db.query(BlockSet)\
        .filter(BlockSet.id == block_set_id).first()


def get_time_frame(db: Session, time_frame_id: int):
    return db.query(TimeFrame)\
        .filter(TimeFrame.id == time_frame_id).first()


def get_time_frames(db: Session):
    return db.query(TimeFrame)


def get_time_frames_by_block_set(db: Session, block_set_id: int):
    return db.query(BlockSet).join(BlockSet.applications)\
        .filter(BlockSet.id == block_set_id)
