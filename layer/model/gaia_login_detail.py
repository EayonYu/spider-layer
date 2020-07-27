from layer.model._base import BaseModel
from layer.model._base import CommonModel

from sqlalchemy import Column, String, Text, Boolean, UniqueConstraint


class GaiaLoginDetailModel(BaseModel, CommonModel):
    __tablename__ = 'gaia_login_detail'

    account_system_id = Column('account_system_id', String(63), nullable=False)
    login_account_id = Column('login_account_id', String(63), nullable=False)
    platform_user_id = Column('platform_user_id', String(255), nullable=False)

    __table_args__ = (UniqueConstraint('account_system_id', 'login_account_id', name='_account_system_id_login_account_id_uc'),)
