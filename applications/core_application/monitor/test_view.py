from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class MonitorTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_monitor(self):
        response = self.client.get("/api/v1/monitor/health_check/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
