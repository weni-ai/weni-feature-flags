from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response


class FeatureFlagsWebhookView(APIView):
    def post(self, request: Request) -> Response:
        # TODO
        return Response(status=200)
