import os
import sys

sys.path.append(os.path.abspath("lib"))

extensions = ["sphinxcontrib.datatemplates"]
templates_path = ["templates"]
template_bridge = "template_bridge.CustomTemplateLoader"
