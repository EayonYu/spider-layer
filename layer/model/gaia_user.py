from ._base import BaseModel
from ._base import CommonModel

from sqlalchemy import Column, String, Text, Boolean, UniqueConstraint


class PartnerUserModel(BaseModel, CommonModel):
    __tablename__ = 'gaia_user'

    platform_user_id = Column('platform_user_id', String(63), nullable=False)
    update_required = Column('update_required', Boolean, nullable=False, default=False)
    immutable_identity = Column('immutable_identity', String(255), nullable=False)
    json_data = Column('json_data', Text)
    sso_id = Column('sso_id', String(63))

    __table_args__ = (UniqueConstraint('platform_user_id', name='_platform_user_id_uc'),)
