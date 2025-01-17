from ..errors import Errors
from ..constants import Constants
from ..log_manager import LogManager

class CommonValidator:

    def __init__(self):
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def list_validate(self,
                      list1:list, 
                      list2:list, 
                      missing_error:str, 
                      *args):
        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="List validating",
                status="Starting",
                details=f"Expected list: {list1} ; Current list: {list2}"
            )
        )
        if not list1:
            return
        if list1 and not list2:
            return
        if not list2:
            raise ValueError(Errors.ELEMENT_MISSING.format(list1))
        for expected_element in list1:
            if expected_element not in list2:
                raise ValueError(missing_error.format(expected_element, *args))
    
    def dict_validate(self,
                      dict1:dict, 
                      dict2:dict,
                      missing_error:str,
                      mismatch_error:str):
        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Dict validating",
                status="Starting",
                details=f"Expected dict: {dict1} ; Current dict: {dict2}"
            )
        )
        if not dict1:
            return
        if not dict2:
            raise ValueError(missing_error.format(dict1))
        for expected_key, expected_value in dict1.items():
            if expected_key in dict2:
                if expected_value != dict2[expected_key]:
                    raise ValueError(mismatch_error.format(expected_key, expected_value, dict2[expected_key]))
            else:
                raise ValueError(missing_error.format(expected_key))
        return True