from enum import Enum, unique


@unique
class Env(Enum):
    LOCAL = 'local'
    DEV = 'dev'
    TEST = 'test'
    PROD = 'prod'
