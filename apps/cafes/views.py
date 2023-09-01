from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.cafes.models import Cafe
from apps.cafes.serializers import CafeSerializer


class CafeAPIViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
