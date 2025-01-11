class CommonValidator:

    def list_validate(self,
                      list1:list, 
                      list2:list, 
                      missing_error:str, 
                      *args):
        if not list1:
            return
        for expected_element in list1:
            if expected_element not in list2:
                raise ValueError(missing_error.format(expected_element, *args))
    
    def dict_validate(self,
                      dict1:dict, 
                      dict2:dict,
                      missing_error:str,
                      mismatch_error:str):
        if not dict1:
            return
        for expected_key, expected_value in dict1.items():
            if expected_key in dict2:
                if expected_value != dict2[expected_key]:
                    raise ValueError(mismatch_error.format(expected_key, expected_value, dict2[expected_key]))
            else:
                raise ValueError(missing_error.format(expected_key))