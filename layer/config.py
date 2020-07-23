from .aws import AWS
from .env import Env


class ServiceProxy:
    def __init__(self, env: Env, aws: AWS):
        self._env = env
        self._aws = aws

        if self._env == Env.LOCAL:
            self.endpoint = '54.222.188.176:8081'
        elif self._env == Env.DEV:
            self.endpoint = self._aws.ssm_client.get_parameter(
                Name=f'/{self._env.value}/service/proxy/endpoint',
                WithDecryption=False
            )['Parameter']['Value']
        elif self._env == Env.TEST:
            raise EnvironmentError
        elif self._env == Env.PROD:
            raise EnvironmentError
        else:
            raise EnvironmentError


class Service:
    def __init__(self, env: Env, aws: AWS):
        self._env = env
        self._aws = aws
        self.proxy = ServiceProxy(env, self._aws)


class Config:
    def __init__(self, env: Env, aws: AWS):
        self._env = env
        self._aws = aws
        self.service = Service(self._env, self._aws)
