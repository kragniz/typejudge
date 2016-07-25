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

for f in [test.greeting, test.testing1, test.TestClass, test.TestClassNoInit]:
    print(f)
    if inspect.isclass(f):
        r = represent_type_hints_class(f)
    else:
        r = represent_type_hints_func(f)

    print(r)
