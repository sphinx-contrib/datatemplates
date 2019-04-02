from sphinx.util import logging

from sphinxcontrib.datatemplates import directive

LOG = logging.getLogger(__name__)


def setup(app):
    LOG.info('initializing sphinxcontrib.datatemplates')
    app.add_directive('datatemplate', directive.DataTemplate)
