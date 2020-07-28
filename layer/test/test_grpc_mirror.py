import unittest

from layer import Layer
from layer import config
from layer.protocol.mirror.python.ping_pb2 import PingRequest


class TestGrpcMirror(unittest.TestCase):

    def test_mirror(self):
        l = Layer(config.Env.DEV)
        mirror_client = l.grpc_mirror_client()
        response = mirror_client.Ping(PingRequest())
        print(response)

if __name__ == '__main__':
    unittest.main()
