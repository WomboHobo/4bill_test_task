from rest_framework.response import Response
from rest_framework.views import APIView

from utils.mixins import CheckAmountMixIn


class ResultView(CheckAmountMixIn, APIView):

    def get(self, request, amount, **kwargs):
        return Response({"result": "OK"})
