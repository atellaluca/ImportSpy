from ..models import Runtime

class RuntimeValidator:
    
    def validate(self, runtime_1: Runtime, runtime_2: Runtime):
        if not runtime_1:
            return
        if runtime_1 and not runtime_2:
            return True
        if not runtime_2:
            return False
        if runtime_1.arch == runtime_2.arch:
            return True
        return False
