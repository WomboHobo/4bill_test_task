import uuid

from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response

from bill_test_proj import settings
from utils.exceptions import AmountReachedException


class CheckAmountMixIn:

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        for key, value in settings.AMOUNT_LIMITS_CONFIG.items():
            amount_sum = 0
            amount_sum_keys = cache.keys(f'{value}_amount_*')
            for cache_key in amount_sum_keys:
                amount_sum += int(cache.get(cache_key))
            if (amount_sum + int(kwargs['amount'])) > key:
                raise AmountReachedException(
                    f'Violated {key} amounts per {value} restriction'
                )

    def finalize_response(self, request, response, *args, **kwargs):
        res = super().finalize_response(request, response, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            for value in settings.AMOUNT_LIMITS_CONFIG.values():
                cache.set(
                    f'{value}_amount_{uuid.uuid4()}',
                    kwargs['amount'],
                    timeout=value.total_seconds()
                )
        return res

