import pytest

from pathlib import Path
from sphinx import version_info as sphinx_version_info

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir():
    """
    Fixture for 'pytest.mark.sphinx'.

    Test data is stored in the 'testdata/test-<testroot>'.
    """
    if sphinx_version_info >= (7, 2):
        abs_path = Path(__file__).parent.absolute()
    else:
        from sphinx.testing.path import path

        abs_path = path(__file__).parent.abspath()

    return abs_path / "testdata"
