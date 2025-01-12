from ..constants import Constants
from ..errors import Errors

class AnnotationValidatorMixin:

    @staticmethod
    def validate_annotation(value: str) -> str:
        if value and value.split("[")[0] not in Constants.SUPPORTED_ANNOTATIONS:
            raise ValueError(Errors.INVALID_ANNOTATION.format(Constants.SUPPORTED_ANNOTATIONS))
        return value