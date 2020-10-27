import importlib

MYSELF = 'promebuilder_template'


def test_import():
    pkg = importlib.import_module(MYSELF)
    assert dir(pkg)
    assert pkg.__name__ == MYSELF
