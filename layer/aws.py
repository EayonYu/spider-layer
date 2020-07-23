import boto3


class AWS:
    def __init__(self):
        self._ssm_client = None
        self._kinesis_client = None

    @property
    def ssm_client(self):
        if not self._ssm_client:
            self._ssm_client = boto3.client("ssm")
        return self._ssm_client

    @property
    def kinesis_client(self):
        if not self._kinesis_client:
            self._kinesis_client = boto3.client('kinesis')
        return self._kinesis_client
