import uuid

from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response

from bill_test_proj import settings
from bill_test_proj.exceptions import AmountReachedException


class CheckAmountMixIn:

    def check_amount_sum(self, amount):
        for key, value in settings.AMOUNT_LIMITS_CONFIG['amount'].items():
            amount_sum = 0
            amount_sum_keys = cache.keys(f'{value}_amount_*')
            for cache_key in amount_sum_keys:
                amount_sum += int(cache.get(cache_key))
            if (amount_sum + int(amount)) > key:
                raise AmountReachedException

    def handle_exception(self, exc):
        if isinstance(exc, AmountReachedException):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return super().handle_exception(self, exc)

    def add_new_amount(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK:
            for value in settings.AMOUNT_LIMITS_CONFIG['amount'].values():
                cache.set(
                    f'{value}_amount_{uuid.uuid4()}',
                    kwargs['amount'],
                    timeout=value.total_seconds()
                )

