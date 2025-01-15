from ..models import Runtime

class RuntimeValidator:
    
    def validate(self, runtime_1: Runtime, runtime_2: Runtime):
        if runtime_1.arch == runtime_2.arch:
            return True
        return False
