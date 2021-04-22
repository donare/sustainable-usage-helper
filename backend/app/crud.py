from sqlalchemy.orm import Session

from . import models, schemas

from datetime import datetime as dt

LIMIT = 100


def get_application(db: Session, application_id: int) ->models.Application:
    return db.query(models.Application)\
        .filter(models.Application.id == application_id).first()


def get_application_by_path(db: Session, application_path: str) ->models.Application:
    return db.query(models.Application) \
        .filter(models.Application.app_path == application_path).first()


def get_applications(db: Session):
    return db.query(models.Application).limit(LIMIT).all()


def get_applications_by_block_set(db: Session, block_set_id: int):
    return db.query(models.Application)\
        .join(models.Application.block_sets)\
        .filter(models.BlockSet.id == block_set_id)\
        .all()


def get_blocked_applications(db: Session):
    now = dt.now()
    time_now = now.time()
    weekday = now.weekday()
    weekday_mask = 1 << weekday

    return db.query(models.Application)\
        .join(models.Application.block_sets)\
        .join(models.BlockSet.time_frames)\
        .filter(models.TimeFrame.start_time >= time_now)\
        .filter(models.TimeFrame.end_time <= time_now)\
        .filter(models.TimeFrame.weekdays & weekday_mask)


def create_application(db: Session, application: schemas.ApplicationCreate):
    db_app = models.Application(app_path=application.app_path)
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


def get_block_sets(db: Session):
    return db.query(models.BlockSet).limit(LIMIT).all()


def get_block_set(db: Session, block_set_id: int) -> models.BlockSet:
    return db.query(models.BlockSet)\
        .filter(models.BlockSet.id == block_set_id).first()


def create_block_set(db: Session, block_set: schemas.BlockSetCreate):
    db_block_set = models.BlockSet(name=block_set.name)
    # Wie auf Applikationen verweisen?
    # Wie auf time_frames verweisen?
    db.add(db_block_set)
    db.commit()
    db.refresh(db_block_set)
    return db_block_set


def get_time_frame(db: Session, time_frame_id: int) -> models.TimeFrame:
    return db.query(models.TimeFrame)\
        .filter(models.TimeFrame.id == time_frame_id).first()


def get_time_frames(db: Session):
    return db.query(models.TimeFrame).limit(LIMIT).all()


def get_time_frames_by_block_set(db: Session, block_set_id: int):
    return db.query(models.BlockSet).join(models.BlockSet.time_frames)\
        .filter(models.BlockSet.id == block_set_id)


def create_time_frame(db: Session, time_frame: schemas.TimeFrameCreate, block_set_id: int):
    # db_time_frame = models.TimeFrame(**time_frame.dict(), block_set_id=block_set_id)
    db_time_frame = models.TimeFrame(**time_frame.dict())
    db.add(db_time_frame)
    block_set = get_block_set(db, block_set_id)
    block_set.time_frames.append(db_time_frame)
    db.commit()
    db.refresh(db_time_frame)
    return db_time_frame


def remove_time_frame(db: Session, time_frame_id: int):
    time_frame = get_time_frame(db, time_frame_id)
    db.delete(time_frame)
    db.commit()


def block_application(db: Session, app_id, block_set_id):
    app = get_application(db, app_id)
    block_set = get_block_set(db, block_set_id)
    block_set.applications.append(app)
    db.add(block_set)  # probably unnecessary
    db.commit()


def unblock_application(db: Session, app_id, block_set_id):
    app = get_application(db, app_id)
    block_set = get_block_set(db, block_set_id)
    block_set.applications.remove(app)

    # Todo: Is explicit deletion of orphans necessary? Or can this be set done automatically?

    db.add(block_set)  # probably unnecessary
    db.commit()
