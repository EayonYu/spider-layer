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
            _me_service_gateway = me_service.get('gateway', '')

        requirements = spec.get('requirements', None)
        if requirements:
            requirements_path = requirements.get('path', '')
            if requirements_path:
                local_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), context))
                abs_requirements_path = os.path.abspath(os.path.join(local_dir, requirements_path))
                abs_requirements_parent_path = os.path.abspath(
                    os.path.dirname(abs_requirements_path)
                )
                subprocess.call(
                    ['rm', '-rf', abs_requirements_path]
                )
                print(abs_requirements_path, 'deleted')

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


def main():
    args = parser.parse_args()
    if args.pull:
        pull()
    elif args.clean:
        clean()
    else:
        return


if __name__ == '__main__':
    main()
