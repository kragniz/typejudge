import argparse
import inspect
import json
import sys
import typing

from typing import Any, Dict, Callable

import semver


def represent_type_hints_func(f: Callable) -> Dict[str, str]:
    d = {}
    for name, value in typing.get_type_hints(f).items():
        d.update({name: str(value)})
    return d


def represent_type_hints_class(obj: Any) -> Dict[str, Dict]:
    d = {}
    for name, method in inspect.getmembers(obj):
        try:
            hints = represent_type_hints_func(method)
            if hints:
                d.update({name: hints})
        except:
            pass
    return d


def represent_type_hints_module(module) -> Dict[str, Dict]:
    types = {}
    for name, obj in module.__dict__.items():
        if inspect.isclass(obj):
            hints = represent_type_hints_class(obj)
        else:
            try:
                hints = represent_type_hints_func(obj)
            except AttributeError:
                hints = {}
        if hints:
            types.update({name: hints})

    return types


def judge(previous: Dict, current: Dict) -> str:
    # ew this code right here someone rewrite it please
    return_value = 0
    for key, value in previous.items():
        diff = 0
        if isinstance(value, dict):
            diff = judge(previous.get(key), current.get(key, {}))
        else:
            if value != current.get(key):
                diff = 2

        if diff > return_value:
            return_value = diff

    for key, value in current.items():
        if key not in previous.keys():
            if return_value == 0:
                return_value = 1

    return return_value


def main():
    parser = argparse.ArgumentParser(description='judge your types')
    parser.add_argument('module', metavar='MODULE', default=None,
                        help='module to import and check')
    parser.add_argument('version', nargs='?', metavar='VERSION', default=None,
                        help='current version of the package')
    parser.add_argument('-o', '--out', default=None,
                        help='save current type definitions to this file')
    parser.add_argument('-f', '--file', default=None,
                        help='load type definitions from this file')
    args = parser.parse_args()

    m = __import__(args.module)

    previous_types = None
    if args.file is not None:
        with open(args.file) as f:
            previous_types = json.load(f)

    types = represent_type_hints_module(m)

    if previous_types:
        judgement = judge(previous_types, types)
        if args.version:
            v = args.version
            if judgement == 0:
                v = semver.bump_patch(v)
            elif judgement == 1:
                v = semver.bump_minor(v)
            elif judgement == 2:
                v = semver.bump_major(v)
            print(v)
        else:
            print({0: 'patch', 1: 'minor', 2: 'major'}.get(judgement))

    if args.out:
        if args.out != '-':
            with open(args.out, 'w') as f:
                json.dump(types, f, sort_keys=True, indent=4)
        else:
            print(json.dumps(types, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
