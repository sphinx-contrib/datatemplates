from sphinx.domains import Domain
from . import directive


class DataTemplateDomain(Domain):

    name = 'datatemplate'
    label = 'DataTemplate Replacement'
    directives = {
        'json': directive.DataTemplateJSON,
        'yaml': directive.DataTemplateYAML,
        'csv': directive.DataTemplateCSV,
        'xml': directive.DataTemplateXML,
        'scandir': directive.DataTemplateScandir,
    }

    def get_objects(self):
        return []

    def resolve_xref(self, env, fromdocname, builder, typ, target, node,
                     contnode):
        return None
