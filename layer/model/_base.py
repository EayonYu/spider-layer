import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base


BaseModel = declarative_base()


class CommonModel:

    id = Column(Integer, primary_key=True)

    created_at = Column('created_at', TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column('updated_at', TIMESTAMP, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow)
    # soft delete
    deleted_at = Column('deleted_at', TIMESTAMP)
    # optimistic lock
    version_id = Column(Integer, nullable=False)
    __mapper_args__ = {
        "version_id_col": version_id
    }
