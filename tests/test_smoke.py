import sys


def test_import_math():
    sys.modules.pop('math', None)
    import math
    assert "math" in sys.modules
