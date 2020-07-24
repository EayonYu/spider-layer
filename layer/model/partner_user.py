from ._base import BaseModel
from ._base import CommonModel

from sqlalchemy import Column, String, Text, Boolean, UniqueConstraint


class PartnerUserModel(BaseModel, CommonModel):
    __tablename__ = 'partner_user'

    partner_id = Column('partner_id', String(63), nullable=False)
    partner_user_id = Column('partner_user_id', String(63), nullable=False)

    update_required = Column('update_required', Boolean, nullable=False, default=False)
    immutable_identity = Column('immutable_identity', String(255), nullable=False)
    json_data = Column('json_data', Text)
    mapping_mode = Column('mapping_mode', String(63))

    # TODO foreign key
    platform_user_id = Column('platform_user_id', String(63))

    __table_args__ = (UniqueConstraint('partner_id', 'partner_user_id', name='_partner_id_partner_user_id_uc'),)
