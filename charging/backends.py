from django.contrib.auth.backends import BaseBackend
from .models import EVStation

class StationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            station = EVStation.objects.get(uname=username, passw=password)
            return station
        except EVStation.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return EVStation.objects.get(pk=user_id)
        except EVStation.DoesNotExist:
            return None
