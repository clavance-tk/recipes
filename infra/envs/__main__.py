# type: ignore
# Dependencies
from tk_create.config.dependencies import load_core_dependencies
from tk_create.config.provider import get_providers
from tk_create.infra.use_cases.http_api_lambda.resources_manager import TkCreateResourcesManager

"""
Project initialization
"""

load_core_dependencies()

# Initialize Pulumi providers
get_providers()

# Create / manage resources

""" Process the Yaml file and create the resources the engineers requires"""
t = TkCreateResourcesManager()
t.create_aws_resources()
t.wire_aws_resources()
