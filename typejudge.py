import argparse
import inspect
import json
import sys
import typing


def represent_type_hints_func(f):
    d = {}
    for name, value in typing.get_type_hints(f).items():
        d.update({name: str(value)})
    return d


def represent_type_hints_class(obj):
    d = {}
    for name, method in inspect.getmembers(obj):
        try:
            d.update({name: represent_type_hints_func(method)})
        except:
            pass
    return d


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='judge your types')
    parser.add_argument('module', metavar='MODULE', default=None,
                        help='module to import and check')
    args = parser.parse_args()

    m = __import__(args.module)

    d = {}
    for name, obj in m.__dict__.items():
        if inspect.isclass(obj):
            hints = represent_type_hints_class(obj)
        else:
            try:
                hints = represent_type_hints_func(obj)
            except AttributeError:
                hints = {}
        if hints:
            d.update({name: hints})
    print(json.dumps(d, sort_keys=True, indent=4))
