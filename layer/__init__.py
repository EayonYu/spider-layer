from .aws import AWS
from .config import Env, Config


class Layer:
    def __init__(self, env: Env):
        self.env = env
        self.aws = AWS()

        self.config = Config(self.env, self.aws)

