from sphinxcontrib.datatemplates import directive


def setup(app):
    app.info('initializing sphinxcontrib.datatemplates')
    app.add_directive('datatemplate', directive.DataTemplate)
