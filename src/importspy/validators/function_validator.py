from ..models import Function
from ..errors import Errors
from typing import List

class FunctionValidator:

    def validate(self,
                 functions_1:List[Function],
                 functions_2:List[Function],
                 classname:str="",
                 *args):
        if not functions_1:
            return
        if functions_1 and not functions_2:
            return True
        if not functions_2:
            return False
        for function_1 in functions_1:
            if function_1 not in functions_2:
                raise ValueError(Errors.FUNCTIONS_MISSING.format(
                    "Method" 
                    if classname 
                    else "", 
                    function_1.name,
                    "Class:" 
                    if classname
                    else "", 
                    classname
                    )
                )
        for function_1 in functions_1:
            function_2 =  next((func for func in functions_2 if func.name == function_1.name), None)
            if function_1.return_annotation and \
                function_1.return_annotation != function_2.return_annotation:
                raise ValueError(Errors.ANNONATION_MISMATCH.format(*args, function_1.name))
            

