from ._base import BaseModel
from ._base import CommonModel

from sqlalchemy import Column, String, Text, Boolean, UniqueConstraint


class GaiaDeviceModel(BaseModel, CommonModel):
    __tablename__ = 'gaia_device'

    platform_device_id = Column('platform_device_id', String(63), nullable=False)
    update_required = Column('update_required', Boolean, nullable=False, default=False)
    immutable_identity = Column('immutable_identity', String(255), nullable=False)
    device_info = Column('device_info', Text)

    __table_args__ = (UniqueConstraint('platform_device_id', name='_platform_device_id_uc'),)
