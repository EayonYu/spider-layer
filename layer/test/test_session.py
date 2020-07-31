import unittest

from sqlalchemy import and_

from layer import Layer
from layer import config
from layer.model import PartnerUserModel
from layer.model import GaiaUserDeviceBindings


class TestSession(unittest.TestCase):

    def test_session(self):
        l = Layer(config.Env.DEV)
        session = l.session()
        partner_user = PartnerUserModel()
        partner_user.partner_id = '1'
        partner_user.partner_user_id = '2'
        partner_user.json_data = '{"hello":"world"}'
        partner_user.immutable_identity = "test"
        session.add(partner_user)
        session.commit()
        session.close()

    def test_session_rollback(self):
        l = Layer(config.Env.DEV)
        session = l.session()

        try:
            partner_user = PartnerUserModel()
            partner_user.partner_id = '1'
            partner_user.partner_user_id = '2'
            partner_user.json_data = '{"hello":"world"}'
            partner_user.immutable_identity = "test"
            session.add(partner_user)
            assert (False)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()

    def test_session_gaia_bindings(self):
        l = Layer(config.Env.DEV)
        session = l.session()
        current_local_gaia_bindings = session.query(GaiaUserDeviceBindings).filter(
                and_(
                        GaiaUserDeviceBindings.platform_user_id.is_("10"),
                        )
                ).all()
        print(current_local_gaia_bindings)


if __name__ == '__main__':
    unittest.main()
