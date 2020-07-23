from enum import Enum, unique


@unique
class Code(Enum):
    SUCCESS = (200, "SUCCESS")
