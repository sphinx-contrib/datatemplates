import pathlib

from sphinxcontrib.datatemplates import loaders


def get_source_path(source):
    return (pathlib.Path('doc') / 'source' / source).resolve()


def test_load_csv():
    source = 'sample.csv'
    abs_path = get_source_path(source)
    with loaders.load_csv(source, abs_path, dialect='excel-tab') as data:
        assert len(data) == 4
        assert data[0] == ['a', 'b', 'c']
