import grpc

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import Session

from .aws import AWS
from .config import Env, Config
from .protocol.mirror.python import mirror_service_pb2_grpc


class Layer:
    def __init__(self, env: Env):
        self.env = env
        self.aws = AWS(self.env)

        self.config = Config(self.env, self.aws)

        self._session_maker = None
        self._grpc_mirror_client = None

    def session(self) -> Session:
        if not self._session_maker:
            engine = create_engine(self.config.db.endpoint, pool_size=70)
            engine.connect()
            self._session_maker = sessionmaker(bind=engine)
        return self._session_maker()

    def grpc_mirror_client(self):
        if not self._grpc_mirror_client:
            channel = grpc.insecure_channel(self.config.service.mirror.endpoint)
            self._grpc_mirror_client = mirror_service_pb2_grpc.MirrorStub(channel)
        return self._grpc_mirror_client
