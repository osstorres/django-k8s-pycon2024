import socket
from celery import shared_task

@shared_task
def hello_task(ignore_result=True):
    print(f"=== Hello from celery application v1 :: host :: {socket.gethostname()}",)
