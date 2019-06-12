from sphinx.util import logging

from . import directive, domain

LOG = logging.getLogger(__name__)


def setup(app):
    LOG.info('initializing sphinxcontrib.datatemplates')
    app.add_directive('datatemplate', directive.DataTemplateLegacy)
    app.add_domain(domain.DataTemplateDomain)

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
