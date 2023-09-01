from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

handler500 = "core.http.exception_handler.server_error"
handler404 = "core.http.exception_handler.not_found"

urlpatterns = [
    # admin site
    path("admin/", admin.site.urls),
    # api
    path("api/v1/", include("apps.authentication.urls"), name="authentication"),
    path("api/v1/", include("apps.cafes.urls"), name="cafes"),
    path("api/v1/", include("apps.products.urls"), name="products"),
    # drf auth
    path("api-auth/", include("rest_framework.urls")),
    # api documentation
    path(
        "docs/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
