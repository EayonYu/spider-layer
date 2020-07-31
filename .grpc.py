import os
import json
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument(
    "--pull", action="store_true", dest="pull", default=False, required=False, help="action: pull"
)
parser.add_argument(
    "--clean", action="store_true", dest="clean", default=False, required=False, help="action: clean"
)
parser.add_argument(
    "--compile", action="store_true", dest="compile", default=False, required=False, help="action: compile"
)
parser.add_argument(
    "--push", action="store_true", dest="push", default=False, required=False, help="action: push"
)

protoc_java_plugin = os.path.abspath(os.path.join(os.path.dirname(__file__), '.protoc-java'))


def pull():
    with open('grpc.json', 'r') as f:
        spec = json.loads(f.read())
        context = spec.get('context', '')
        if not context:
            print('require <context> field')
            return

        source = spec.get('source', None)
        if not source:
            print('require <source> field')
            return

        source_provider = source.get('provider', '')
        source_service = source.get('service', '')
        source_bucket = source.get('bucket', '')
        if not source_provider:
            print('require <source.provider> field')
            return
        if not source_service:
            print('require <source.service> field')
            return
        if source_provider == "aws" and source_service == "s3" and not source_bucket:
            print('require <source.bucket> field')
            return

        me = spec.get('me', None)
        if not me:
            print('require <me> field')
            return
        me_name = me.get('name', '')
        if not me_name:
            print('require <me.name> field')
            return
        me_path = me.get('path', '')
        if not me_path:
            print('require <me.path> field')
            return

        me_service = me.get('service', None)
        if me_service:
            me_service_version = me_service.get('version', '')
            if not me_service_version:
                print('require <me.service.version> field')
                return
            me_service_proto = me_service.get('proto', '')
            if not me_service_proto:
                print('require <me.service.proto> field')
                return
            _me_service_gateway = me_service.get('gateway', '')

        requirements = spec.get('requirements', None)
        if requirements:
            requirements_path = requirements.get('path', '')
            if not requirements_path:
                print('require <requirements.path> field')
                return
            local_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), context))
            abs_requirements_path = os.path.abspath(os.path.join(local_dir, requirements_path))

            requirements_services = requirements.get('services', [])
            for i in range(0, len(requirements_services)):
                service = requirements_services[i]
                s = service.get('service', '')
                v = service.get('version', '')
                lan = service.get('lan', '')
                target = service.get('target', '')
                if not s or not v or not lan or not target:
                    print('index: %d need more info' % i)
                    continue

                target_dir = os.path.abspath(os.path.join(abs_requirements_path, target))

                if source_provider == 'aws' and source_service == 's3':
                    source_path = source_bucket + '/%s/%s/%s' % (s, v, lan)
                    subprocess.call(
                        ['aws', 's3', 'sync', '--delete', source_path, target_dir]
                    )
                else:
                    print('source provider not support')
                    continue

                # create __init__.py for python packages
                if lan == 'python':
                    p = target_dir
                    while True:
                        if not os.path.commonpath([p, local_dir]) == local_dir:
                            break
                        init_file = os.path.abspath(os.path.join(p, '__init__.py'))
                        if not os.path.exists(init_file):
                            print('create __init__.py file for python package in: ', p)
                            open(init_file, 'a').close()
                        p = os.path.abspath(os.path.dirname(p))



def clean():
    with open('grpc.json', 'r') as f:
        spec = json.loads(f.read())
        context = spec.get('context', '')
        if not context:
            print('require <context> field')
            return

        source = spec.get('source', None)
        if not source:
            print('require <source> field')
            return

        source_provider = source.get('provider', '')
        source_service = source.get('service', '')
        source_bucket = source.get('bucket', '')
        if not source_provider:
            print('require <source.provider> field')
            return
        if not source_service:
            print('require <source.service> field')
            return
        if source_provider == "aws" and source_service == "s3" and not source_bucket:
            print('require <source.bucket> field')
            return

        me = spec.get('me', None)
        if not me:
            print('require <me> field')
            return
        me_name = me.get('name', '')
        if not me_name:
            print('require <me.name> field')
            return
        me_path = me.get('path', '')
        if not me_path:
            print('require <me.path> field')
            return

        me_service = me.get('service', None)
        if me_service:
            me_service_version = me_service.get('version', '')
            if not me_service_version:
                print('require <me.service.version> field')
                return
            me_service_proto = me_service.get('proto', '')
            if not me_service_proto:
                print('require <me.service.proto> field')
                return
            # me_service_gateway = me_service.get('gateway', '')

            local_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), context))
            abs_me_path = os.path.abspath(os.path.join(local_dir, me_path))
            # abs_me_proto_path = os.path.abspath(os.path.join(abs_me_path, me_service_proto))

            abs_me_python_path = os.path.abspath(os.path.join(abs_me_path, 'python'))
            abs_me_go_path = os.path.abspath(os.path.join(abs_me_path, 'go'))
            abs_me_java_path = os.path.abspath(os.path.join(abs_me_path, 'java'))
            abs_me_swagger_path = os.path.abspath(os.path.join(abs_me_path, 'swagger'))
            subprocess.call(
                ['rm', '-rf', abs_me_python_path]
            )
            subprocess.call(
                ['rm', '-rf', abs_me_go_path]
            )
            subprocess.call(
                ['rm', '-rf', abs_me_java_path]
            )
            subprocess.call(
                ['rm', '-rf', abs_me_swagger_path]
            )

        requirements = spec.get('requirements', None)
        if requirements:
            requirements_path = requirements.get('path', '')
            if requirements_path:
                local_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), context))
                abs_requirements_path = os.path.abspath(os.path.join(local_dir, requirements_path))
                subprocess.call(
                    ['rm', '-rf', abs_requirements_path]
                )
                print(abs_requirements_path, 'deleted')

                """
                abs_requirements_parent_path = os.path.abspath(
                    os.path.dirname(abs_requirements_path)
                )
                p = abs_requirements_parent_path
                while True:
                    if not os.path.commonpath([p, local_dir]) == local_dir:
                        break
                    init_file = os.path.abspath(os.path.join(p, '__init__.py'))
                    if os.path.exists(init_file):
                        subprocess.call(
                            ['rm', '-rf', init_file]
                        )
                        print('delete __init__.py file in:', p)
                    p = os.path.abspath(os.path.dirname(p))
                """


def compile_proto():
    with open('grpc.json', 'r') as f:
        spec = json.loads(f.read())
        context = spec.get('context', '')
        if not context:
            print('require <context> field')
            return

        source = spec.get('source', None)
        if not source:
            print('require <source> field')
            return

        source_provider = source.get('provider', '')
        source_service = source.get('service', '')
        source_bucket = source.get('bucket', '')
        if not source_provider:
            print('require <source.provider> field')
            return
        if not source_service:
            print('require <source.service> field')
            return
        if source_provider == "aws" and source_service == "s3" and not source_bucket:
            print('require <source.bucket> field')
            return

        me = spec.get('me', None)
        if not me:
            print('require <me> field')
            return
        me_name = me.get('name', '')
        if not me_name:
            print('require <me.name> field')
            return
        me_path = me.get('path', '')
        if not me_path:
            print('require <me.path> field')
            return

        me_service = me.get('service', None)
        if me_service:
            me_service_version = me_service.get('version', '')
            if not me_service_version:
                print('require <me.service.version> field')
                return
            me_service_proto = me_service.get('proto', '')
            if not me_service_proto:
                print('require <me.service.proto> field')
                return
            me_service_gateway = me_service.get('gateway', '')

            local_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), context))
            abs_me_path = os.path.abspath(os.path.join(local_dir, me_path))
            # abs_me_proto_path = os.path.abspath(os.path.join(abs_me_path, me_service_proto))
            abs_me_python_path = os.path.abspath(os.path.join(abs_me_path, 'python'))
            abs_me_go_path = os.path.abspath(os.path.join(abs_me_path, 'go'))
            abs_me_java_path = os.path.abspath(os.path.join(abs_me_path, 'java'))
            abs_me_swagger_path = os.path.abspath(os.path.join(abs_me_path, 'swagger'))
            env = os.environ.copy()
            google_api_path = env["GOPATH"] + '/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis'

            # compile python protobuf
            # clear
            subprocess.call(['rm', '-rf', abs_me_python_path])
            subprocess.call(['mkdir', abs_me_python_path])
            # compile
            cmd = 'cd {abs_me_path}; python -m grpc_tools.protoc ' \
                  '-I {me_service_proto} -I {google_api_path} ' \
                  '--python_out=./python --grpc_python_out=./python ' \
                  '{me_service_proto}/*.proto; ' \
                  'cd ./python; ' \
                  'sed -i "" -E "s/^import (.+_pb2.*)/from . import \\1/g" *_pb2*.py;'\
                .format(abs_me_path=abs_me_path,
                        me_service_proto=me_service_proto,
                        google_api_path=google_api_path)
            '''
            cmd = f'cd {abs_me_path}; ' \
                  f'python -m grpc_tools.protoc ' \
                  f'-I {me_service_proto} ' \
                  f'-I {google_api_path} ' \
                  f'--python_out=./python ' \
                  f'--grpc_python_out=./python ' \
                  f'{me_service_proto}/*.proto; ' \
                  f'cd ./python; ' \
                  f'sed -i "" -E "s/^import (.+_pb2.*)/from . import \\1/g" *_pb2*.py;'
            '''
            print(cmd)
            os.system(cmd)

            # compile go protobuf
            # clear
            subprocess.call(['rm', '-rf', abs_me_go_path])
            subprocess.call(['mkdir', abs_me_go_path])
            # compile
            cmd = 'cd {abs_me_path}; ' \
                  'protoc ' \
                  '-I {me_service_proto} ' \
                  '-I {google_api_path} ' \
                  '--go_out=plugins=grpc:./go ' \
                  '{me_service_proto}/*.proto; '\
                .format(abs_me_path=abs_me_path,
                        me_service_proto=me_service_proto,
                        google_api_path=google_api_path)
            '''
            cmd = f'cd {abs_me_path}; ' \
                  f'protoc ' \
                  f'-I {me_service_proto} ' \
                  f'-I {google_api_path} ' \
                  f'--go_out=plugins=grpc:./go ' \
                  f'{me_service_proto}/*.proto; '
            '''
            print(cmd)
            os.system(cmd)

            # compile java protobuf
            # clear
            subprocess.call(['rm', '-rf', abs_me_java_path])
            subprocess.call(['mkdir', abs_me_java_path])
            # compile
            cmd = 'cd {abs_me_path}; ' \
                  'protoc --plugin=protoc-gen-grpc-java={protoc_java_plugin} ' \
                  '-I {me_service_proto} ' \
                  '-I {google_api_path} ' \
                  '--grpc-java_out=./java ' \
                  '--java_out=./java ' \
                  '{me_service_proto}/*.proto; '\
                .format(abs_me_path=abs_me_path,
                        me_service_proto=me_service_proto,
                        protoc_java_plugin=protoc_java_plugin,
                        google_api_path=google_api_path)
            '''
            cmd = f'cd {abs_me_path}; ' \
                  f'protoc --plugin=protoc-gen-grpc-java={protoc_java_plugin} ' \
                  f'-I {me_service_proto} ' \
                  f'-I {google_api_path} ' \
                  f'--grpc-java_out=./java ' \
                  f'--java_out=./java ' \
                  f'{me_service_proto}/*.proto; '
            '''
            print(cmd)
            os.system(cmd)

            # compile swagger
            # clear
            subprocess.call(['rm', '-rf', abs_me_swagger_path])
            subprocess.call(['mkdir', abs_me_swagger_path])
            # compile
            cmd = 'cd {abs_me_path}; ' \
                  'protoc ' \
                  '-I {me_service_proto} ' \
                  '-I {google_api_path} ' \
                  '--swagger_out=logtostderr=true:./swagger ' \
                  '{me_service_proto}/*.proto; '\
                .format(abs_me_path=abs_me_path,
                        me_service_proto=me_service_proto,
                        google_api_path=google_api_path)
            '''
            cmd = f'cd {abs_me_path}; ' \
                  f'protoc ' \
                  f'-I {me_service_proto} ' \
                  f'-I {google_api_path} ' \
                  f'--swagger_out=logtostderr=true:./swagger ' \
                  f'{me_service_proto}/*.proto; '
            '''
            print(cmd)
            os.system(cmd)

            # compile gateway
            # clear
            if me_service_gateway:
                abs_me_gateway_path = os.path.abspath(os.path.join(abs_me_path, me_service_gateway))
                subprocess.call(['rm', '-rf', abs_me_gateway_path])
                subprocess.call(['mkdir', abs_me_gateway_path])
                abs_me_go_files = os.path.abspath(os.path.join(abs_me_go_path, '*'))
                cmd = 'cp {abs_me_go_files} {abs_me_gateway_path}'.format(
                    abs_me_go_files=abs_me_go_files,
                    abs_me_gateway_path=abs_me_gateway_path
                )
                print(cmd)
                os.system(cmd)

                # compile
                cmd = 'cd {abs_me_path}; ' \
                      'protoc ' \
                      '-I {me_service_proto} ' \
                      '-I {google_api_path} ' \
                      '--grpc-gateway_out=logtostderr=true:{abs_me_gateway_path} ' \
                      '{me_service_proto}/*.proto; '\
                    .format(abs_me_path=abs_me_path,
                            me_service_proto=me_service_proto,
                            google_api_path=google_api_path,
                            abs_me_gateway_path=abs_me_gateway_path)
                '''
                cmd = f'cd {abs_me_path}; ' \
                      f'protoc ' \
                      f'-I {me_service_proto} ' \
                      f'-I {google_api_path} ' \
                      f'--grpc-gateway_out=logtostderr=true:{abs_me_gateway_path} ' \
                      f'{me_service_proto}/*.proto; '
                '''
                print(cmd)
                os.system(cmd)


def push():
    with open('grpc.json', 'r') as f:
        spec = json.loads(f.read())
        context = spec.get('context', '')
        if not context:
            print('require <context> field')
            return

        source = spec.get('source', None)
        if not source:
            print('require <source> field')
            return

        source_provider = source.get('provider', '')
        source_service = source.get('service', '')
        source_bucket = source.get('bucket', '')
        if not source_provider:
            print('require <source.provider> field')
            return
        if not source_service:
            print('require <source.service> field')
            return
        if source_provider == "aws" and source_service == "s3" and not source_bucket:
            print('require <source.bucket> field')
            return

        me = spec.get('me', None)
        if not me:
            print('require <me> field')
            return
        me_name = me.get('name', '')
        if not me_name:
            print('require <me.name> field')
            return
        me_path = me.get('path', '')
        if not me_path:
            print('require <me.path> field')
            return

        me_service = me.get('service', None)
        if me_service:
            me_service_version = me_service.get('version', '')
            if not me_service_version:
                print('require <me.service.version> field')
                return
            me_service_proto = me_service.get('proto', '')
            if not me_service_proto:
                print('require <me.service.proto> field')
                return
            # me_service_gateway = me_service.get('gateway', '')

            local_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), context))
            abs_me_path = os.path.abspath(os.path.join(local_dir, me_path))

            abs_me_proto_path = os.path.abspath(os.path.join(abs_me_path, me_service_proto))
            abs_me_python_path = os.path.abspath(os.path.join(abs_me_path, 'python'))
            abs_me_go_path = os.path.abspath(os.path.join(abs_me_path, 'go'))
            abs_me_java_path = os.path.abspath(os.path.join(abs_me_path, 'java'))
            abs_me_swagger_path = os.path.abspath(os.path.join(abs_me_path, 'swagger'))

            proto_source_path = '{source_bucket}/{me_name}/{me_service_version}/proto'.format(
                source_bucket=source_bucket,
                me_name=me_name,
                me_service_version=me_service_version
            )
            subprocess.call(
                ['aws', 's3', 'sync', '--delete', abs_me_proto_path, proto_source_path]
            )
            python_source_path = '{source_bucket}/{me_name}/{me_service_version}/python'.format(
                source_bucket=source_bucket,
                me_name=me_name,
                me_service_version=me_service_version
            )
            subprocess.call(
                ['aws', 's3', 'sync', '--delete', abs_me_python_path, python_source_path]
            )
            go_source_path = '{source_bucket}/{me_name}/{me_service_version}/go'.format(
                source_bucket=source_bucket,
                me_name=me_name,
                me_service_version=me_service_version
            )
            subprocess.call(
                ['aws', 's3', 'sync', '--delete', abs_me_go_path, go_source_path]
            )
            java_source_path = '{source_bucket}/{me_name}/{me_service_version}/java'.format(
                source_bucket=source_bucket,
                me_name=me_name,
                me_service_version=me_service_version
            )
            subprocess.call(
                ['aws', 's3', 'sync', '--delete', abs_me_java_path, java_source_path]
            )
            swagger_source_path = '{source_bucket}/{me_name}/{me_service_version}/swagger'.format(
                source_bucket=source_bucket,
                me_name=me_name,
                me_service_version=me_service_version
            )
            subprocess.call(
                ['aws', 's3', 'sync', '--delete', abs_me_swagger_path, swagger_source_path]
            )


def main():
    args = parser.parse_args()
    if args.pull:
        pull()
    elif args.clean:
        clean()
    elif args.compile:
        compile_proto()
    elif args.push:
        push()
    else:
        return


if __name__ == '__main__':
    main()
