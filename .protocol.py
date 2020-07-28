import os
import json
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument(
    "-p", "--pull", action="store_true", dest="pull", default=False, required=False, help="action: pull"
)
parser.add_argument(
    "-c", "--clean", action="store_true", dest="clean", default=False, required=False, help="action: clean"
)


def pull():
    with open('protocol.json', 'r') as f:
        spec = json.loads(f.read())
        source = spec.get('source', '')
        local = spec.get('local', '')
        requirements = spec.get('requirements', [])
        if not source or not local:
            print('require <source>, <local> field')
            return

        for i in range(0, len(requirements)):
            requirement = requirements[i]
            service = requirement.get('service', '')
            version = requirement.get('version', '')
            lan = requirement.get('lan', '')
            target = requirement.get('target', '')
            if not service or not version or not lan or not target:
                print('index: %d need more info' % i)
                continue
            local_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), local))
            target_dir = os.path.abspath(os.path.join(local_dir, target))
            source_path = source + '/%s/%s/%s' % (service, version, lan)

            subprocess.call(
                ['aws', 's3', 'sync', '--delete', source_path, target_dir]
            )


def clear():
    with open('protocol.json', 'r') as f:
        spec = json.loads(f.read())
        source = spec.get('source', '')
        local = spec.get('local', '')
        requirements = spec.get('requirements', [])
        if not source or not local:
            print('require <source>, <local> field')
            return

        for i in range(0, len(requirements)):
            requirement = requirements[i]
            service = requirement.get('service', '')
            version = requirement.get('version', '')
            lan = requirement.get('lan', '')
            target = requirement.get('target', '')
            if not service or not version or not lan or not target:
                print('index: %d need more info' % i)
                continue
            local_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), local))
            target_dir = os.path.abspath(os.path.join(local_dir, target))

            subprocess.call(
                ['rm', '-rf', target_dir]
            )


def clean():
    with open('protocol.json', 'r') as f:
        spec = json.loads(f.read())
        source = spec.get('source', '')
        local = spec.get('local', '')
        if not source or not local:
            print('require <source>, <local> field')
            return
        local_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), local))
        files = os.listdir(local_dir)
        for file in files:
            path = os.path.abspath(os.path.join(local_dir, file))
            if os.path.isdir(path):
                print(path, 'deleted')
                subprocess.call(
                    ['rm', '-rf', path]
                )


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
