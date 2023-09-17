from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from apps.cafes.models import Cafe
from apps.cafes.serializers import CafeSerializer
from apps.products.permissions import IsCafeOwner

TAG = "Cafe API"


@extend_schema(
    tags=[TAG],
)
@extend_schema_view(
    list=extend_schema(
        summary="본인이 소유한 카페 목록을 반환합니다.",
        description="본인이 소유한 카페 목록을 반환합니다. Cursor 기반 Pagination을 사용합니다.",
    ),
    create=extend_schema(
        summary="새로운 카페를 생성합니다.",
        description="새로운 카페를 생성합니다. 로그인한 유저만 카페를 생성할 수 있습니다.",
    ),
    retrieve=extend_schema(
        summary="uuid에 해당하는 카페의 상세 정보를 반환합니다.",
        description="uuid에 해당하는 카페의 상세 정보를 반환합니다. 본인이 소유한 카페만 조회할 수 있습니다.",
    ),
    update=extend_schema(
        summary="uuid에 해당하는 카페의 모든 정보를 업데이트합니다.",
        description="uuid에 해당하는 카페의 모든 정보를 업데이트합니다. 본인이 소유한 카페만 업데이트할 수 있습니다.",
    ),
    partial_update=extend_schema(
        summary="uuid에 해당하는 카페의 일부 정보를 업데이트합니다.",
        description="uuid에 해당하는 카페의 일부 정보를 업데이트합니다. 본인이 소유한 카페만 업데이트할 수 있습니다.",
    ),
    destroy=extend_schema(
        summary="uuid에 해당하는 카페를 삭제합니다.",
        description="uuid에 해당하는 카페를 삭제합니다. 본인이 소유한 카페만 삭제할 수 있습니다.",
    ),
)
class CafeAPIViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    lookup_url_kwarg = "cafe_uuid"
    serializer_class = CafeSerializer
    permission_classes = (IsCafeOwner,)

    def get_queryset(self):
        return Cafe.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
