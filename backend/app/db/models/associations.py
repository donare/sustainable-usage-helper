from sqlalchemy import Integer
from sqlalchemy import Column, Table, ForeignKey
from app.db.config import Base


block_associations = Table(
    "block_set_associations",
    Base.metadata,
    Column("apps_id", Integer, ForeignKey("application.id")),
    Column("block_sets_id", Integer, ForeignKey("blockset.id"))
)
