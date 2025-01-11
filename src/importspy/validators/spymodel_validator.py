from ..models import (
    SpyModel,
    Deployment
)
from .deployment_validator import DeploymentValidator
from .module_validator import ModuleValidator

class SpyModelValidator:

    def validate(self,
                  spy_model_1: SpyModel,
                  spy_model_2: SpyModel) -> bool:
        deployment_2:Deployment = spy_model_2.deployments[0]
        DeploymentValidator().validate(spy_model_1.deployments, deployment_2)
        ModuleValidator().validate([spy_model_1], 
                                   spy_model_2
                                   .deployments[0]
                                   .runtimes[0]
                                   .systems[0]
                                   .pythons[0]
                                   .modules[0])