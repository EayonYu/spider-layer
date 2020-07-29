from ._base import BaseModel
from ._base import CommonModel

from sqlalchemy import Column, String, Text, Boolean, UniqueConstraint


class PartnerDeviceModel(BaseModel, CommonModel):
    __tablename__ = 'partner_device'

    partner_id = Column('partner_id', String(63), nullable=False)
    partner_device_id = Column('partner_device_id', String(63), nullable=False)

    update_required = Column('update_required', Boolean, nullable=False, default=False)
    immutable_identity = Column('immutable_identity', String(255), nullable=False)
    device_info = Column('device_info', Text)
    primary_device = Column('primary_device', Boolean, nullable=False)
    mapping_mode = Column('mapping_mode', String(63))

    # TODO foreign key
    platform_device_id = Column('platform_device_id', String(63))

    __table_args__ = (UniqueConstraint('partner_id', 'partner_device_id', name='_partner_id_partner_device_id_uc'),)
