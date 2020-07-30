from sqlalchemy import Column, String, Text, Boolean, UniqueConstraint, Integer

from layer.model._base import BaseModel
from layer.model._base import CommonModel


class PartnerUserDeviceBindings(BaseModel, CommonModel):
    __tablename__ = 'partner_user_device_bindings'

    partner_id = Column('partner_id', String(63), nullable=False)
    partner_user_id = Column('partner_user_id', String(63), nullable=False)
    partner_device_id = Column('partner_device_id', String(63), nullable=False)
    update_required = Column('update_required', Boolean, nullable=False, default=False)
    user_role = Column('user_role', Integer, default=0)
    extra = Column('extra', Text)

    __table_args__ = (
        UniqueConstraint('partner_id', 'partner_user_id', 'partner_device_id', name='_three_uc'),
        {'extend_existing': True})

    def dict(self):
        return {
            'partner_id': self.partner_id,
            'partner_user_id': self.partner_user_id,
            'partner_device_id': self.partner_device_id,
            'user_role': self.user_role,
            'extra': self.extra
            }
