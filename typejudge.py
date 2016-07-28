import sys
import inspect
import typing

import test


def represent_type_hints_func(f):
    return str(typing.get_type_hints(f))


def represent_type_hints_class(obj):
    d = {}
    for name, method in inspect.getmembers(obj):
        try:
            d.update({name: represent_type_hints_func(method)})
        except:
            pass
    return d


if __name__ == '__main__':
    m = __import__(sys.argv[1])
    for name, obj in m.__dict__.items():
        if inspect.isclass(obj):
            hints = represent_type_hints_class(obj)
        else:
            try:
                hints = represent_type_hints_func(obj)
            except AttributeError:
                hints = {}
        if hints:
            print(name, obj, hints)
