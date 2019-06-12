from sphinx.util import logging

from sphinxcontrib.datatemplates import directive

LOG = logging.getLogger(__name__)


def setup(app):
    LOG.info('initializing sphinxcontrib.datatemplates')
    app.add_directive('datatemplate-json', directive.DataTemplateJSON)
    app.add_directive('datatemplate-yaml', directive.DataTemplateYAML)
    app.add_directive('datatemplate-csv', directive.DataTemplateCSV)
    app.add_directive('datatemplate-xml', directive.DataTemplateXML)
    app.add_directive('datatemplate', directive.DataTemplateLegacy)
