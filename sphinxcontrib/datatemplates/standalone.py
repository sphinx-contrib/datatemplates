from . import mixins


class DataTemplateStandalone:
    """
    Mixin for AbstractDataTemplateBase
    """

    def __init__(self, env, options={}):
        self.env = env
        os = self.option_spec
        self.options = {
            k: os[k](v) if k in os else v
            for k, v in options.items()
        }

    def run(self):
        resolved_path = self.options['source']
        template_name = self.options['template']
        template = self.env.get_template(template_name)

        with self._load_data_cm(resolved_path) as data:
            context = self._make_context(data)
            rendered_template = template.render(context)

        return rendered_template


class DataTemplateJSONStandalone(mixins.DataTemplateJSON,
                                 DataTemplateStandalone):
    pass


class DataTemplateCSVStandalone(mixins.DataTemplateCSV,
                                DataTemplateStandalone):
    pass


class DataTemplateYAMLStandalone(mixins.DataTemplateYAML,
                                 DataTemplateStandalone):
    pass


class DataTemplateXMLStandalone(mixins.DataTemplateXML,
                                DataTemplateStandalone):
    pass


class DataTemplateDBMStandalone(mixins.DataTemplateDBM,
                                DataTemplateStandalone):
    pass


class DataTemplateImportModuleStandalone(mixins.DataTemplateImportModule,
                                         DataTemplateStandalone):
    pass


datatemplate_names = {
    "json": DataTemplateJSONStandalone,
    "csv": DataTemplateCSVStandalone,
    "yaml": DataTemplateYAMLStandalone,
    "xml": DataTemplateXMLStandalone,
    "dbm": DataTemplateDBMStandalone,
    "import-module": DataTemplateImportModuleStandalone,
}
