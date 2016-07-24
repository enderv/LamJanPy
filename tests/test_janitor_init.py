from Janitor import Janitor
import pytest


def test_bad_regions():
    with pytest.raises(TypeError) as execinfo:
        Janitor({'regions':1})
    assert 'regions must be a list' in str(execinfo.value)


