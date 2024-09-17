from rest_framework import status, permissions, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class EmptySerializer(serializers.Serializer):
    pass


class HealthView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = EmptySerializer

    def get(self, request):
        return Response("OK", status=status.HTTP_200_OK)
