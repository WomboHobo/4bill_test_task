from rest_framework.exceptions import APIException


class AmountReachedException(APIException):
    status_code = 400
    default_detail = 'Violated amounts per time restriction.'
    default_code = 'restriction_violation'
