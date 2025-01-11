from ..models import Deployment
from .runtime_validator import RuntimeValidator
from typing import List

class DeploymentValidator:

    def validate(self,
                 deployments_1:List[Deployment],
                 deployment_2:Deployment):
        rv = RuntimeValidator()
        for deployment_1 in deployments_1:
            rv.validate(deployment_1.runtimes, deployment_2.runtimes[0])