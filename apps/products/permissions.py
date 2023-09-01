from rest_framework.permissions import IsAuthenticated

from apps.cafes.models import Cafe


class IsCafeOwner(IsAuthenticated):
    def has_permission(self, request, view):
        cafe = Cafe.objects.filter(uuid__exact=view.kwargs["cafe_uuid"]).first()
        if cafe:
            return super().has_permission(request, view) and (
                request.user == cafe.owner
            )

        return super().has_permission(request, view)
