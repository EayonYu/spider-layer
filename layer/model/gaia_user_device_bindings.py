from sqlalchemy import Column, String, Text, UniqueConstraint, Integer

from layer.model._base import BaseModel
from layer.model._base import CommonModel


class GaiaUserDeviceBindings(BaseModel, CommonModel):
    __tablename__ = 'gaia_user_device_bindings'

    platform_user_id = Column('platform_user_id', String(63), nullable=False)
    platform_device_id = Column('platform_device_id', String(63), nullable=False)
    user_role = Column('user_role', Integer, default=0)
    extra = Column('extra', Text)

    __table_args__ = (
        UniqueConstraint('platform_user_id', 'platform_device_id', name='_platform_user_id_platform_device_id_uc'),
        {'extend_existing': True})
