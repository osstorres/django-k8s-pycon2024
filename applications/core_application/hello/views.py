from rest_framework import status, permissions, serializers
from rest_framework.generics import GenericAPIView
import socket
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
import time
import threading

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

def cpu_intensive_task(duration):
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > duration:
            break
        # Busy-wait loop
        start_busy = time.time()
        while time.time() - start_busy < 0.1:  # Busy-wait for 0.1 seconds
            pass
        # Sleep to reduce CPU usage
        time.sleep(0.15)  # Sleep for 0.15 seconds

class LoadView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        threading.Thread(target=cpu_intensive_task, args=(60,)).start()
        return Response(
            "OK",
            status=status.HTTP_200_OK,
        )