from sphinxcontrib.datatemplates import loaders


def test_lookup_json():
    actual = loaders.loader_for_source('source.json')
    assert actual == loaders.load_json


def test_lookup_yaml():
    actual = loaders.loader_for_source('source.yaml')
    assert actual == loaders.load_yaml


def test_lookup_yml():
    actual = loaders.loader_for_source('source.yml')
    assert actual == loaders.load_yaml


def test_lookup_xml():
    actual = loaders.loader_for_source('source.xml')
    assert actual == loaders.load_xml


def test_lookup_csv():
    actual = loaders.loader_for_source('source.csv')
    assert actual == loaders.load_csv


def test_lookup_dbm():
    actual = loaders.loader_for_source('source.dbm')
    assert actual == loaders.load_dbm
