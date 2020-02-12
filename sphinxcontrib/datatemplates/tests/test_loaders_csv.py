from sphinxcontrib.datatemplates import loaders


def test_load_csv():
    source = 'doc/source/sample.csv'
    with loaders.CSVLoader(source, dialect='excel-tab') as data:
        assert len(data) == 4
        assert data[0] == ['a', 'b', 'c']
