from collections.abc import Mapping

import pytest

from pydantic_core import SchemaValidator, ValidationError


def test_dict():
    v = SchemaValidator({'type': 'dict', 'keys': {'type': 'int'}, 'values': {'type': 'int'}})
    assert v.validate_python({'1': 2, '3': 4}) == {1: 2, 3: 4}


def test_dict_any_value():
    v = SchemaValidator({'type': 'dict', 'keys': {'type': 'str'}})
    assert v.validate_python({'1': 1, '2': 'a', '3': None}) == {'1': 1, '2': 'a', '3': None}


def test_mapping():
    class MyMapping(Mapping):
        def __init__(self, d):
            self._d = d

        def __getitem__(self, key):
            return self._d[key]

        def __iter__(self):
            return iter(self._d)

        def __len__(self):
            return len(self._d)

    v = SchemaValidator({'type': 'dict', 'keys': {'type': 'int'}, 'values': {'type': 'int'}})
    assert v.validate_python(MyMapping({'1': 2, 3: '4'})) == {1: 2, 3: 4}


def test_dict_mapping():
    class ClassWithDict:
        def __init__(self):
            self.a = 1
            self.b = 2
            self.c = 'ham'

    v = SchemaValidator({'type': 'dict', 'keys': {'type': 'str'}})
    with pytest.raises(ValidationError, match='Value must be a valid dictionary'):
        v.validate_python(ClassWithDict())

    v = SchemaValidator({'type': 'dict', 'keys': {'type': 'str'}, 'try_instance_as_dict': True})
    assert v.validate_python(ClassWithDict()) == {'a': 1, 'b': 2, 'c': 'ham'}
