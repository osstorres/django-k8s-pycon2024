from rest_framework import status, permissions, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import socket


class EmptySerializer(serializers.Serializer):
    pass


class HostView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = EmptySerializer

    def get(self, request):
        return Response(
            f"Hello from core application v1 :: {socket.gethostname()}",
            status=status.HTTP_200_OK,
        )
