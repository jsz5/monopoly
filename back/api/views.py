from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView

)


class Test(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response("test")
