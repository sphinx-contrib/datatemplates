from sphinx.domains import Domain
from . import directive


class DataTemplateDomain(Domain):

    name = 'datatemplate'
    label = 'DataTemplate Replacement'
    directives = {
        'json': directive.DataTemplateJSONDirective,
        'yaml': directive.DataTemplateYAMLDirective,
        'csv': directive.DataTemplateCSVDirective,
        'xml': directive.DataTemplateXMLDirective,
        'dbm': directive.DataTemplateDBMDirective,
        'import-module': directive.DataTemplateImportModuleDirective,
    }

    def get_objects(self):
        return []

    def resolve_xref(self, env, fromdocname, builder, typ, target, node,
                     contnode):
        return None

    def merge_domaindata(self, docnames, otherdata):
        pass
