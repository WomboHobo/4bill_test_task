from rest_framework.response import Response
from rest_framework.views import APIView

from bill_test_proj.mixins import CheckAmountMixIn


class ResultView(CheckAmountMixIn, APIView):

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.check_amount_sum(**kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        res = super().finalize_response(request, response, *args, **kwargs)
        self.add_new_amount(request, response, *args, **kwargs)
        return res

    def get(self, request, amount, **kwargs):
        return Response({"result": "OK"})
