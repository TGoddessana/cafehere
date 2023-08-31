from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, ListAPIView

from apps.authentication.models import User
from apps.authentication.serializers import RegisterSerializer


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
