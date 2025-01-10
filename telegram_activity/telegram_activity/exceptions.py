from rest_framework import status
from rest_framework.exceptions import APIException

class UnprocessableEntityException(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Unprocessable Entity"
    default_code = "unprocessable_entity"
    
class ConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Conflict detected"
    default_code = "сonflict"