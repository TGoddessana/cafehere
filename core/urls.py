from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

handler500 = "core.http.exception_handler.server_error"
handler404 = "core.http.exception_handler.not_found"

admin.site.site_header = _("Cafehere administration")
admin.site.site_title = _("Cafehere administration")

urlpatterns = [
    # admin site
    path("admin/", admin.site.urls),
    # api
    path("api/v1/", include("apps.authentication.urls"), name="authentication"),
    path("api/v1/cafes/", include("apps.cafes.urls"), name="cafes"),
    path("api/v1/cafes/", include("apps.products.urls"), name="products"),
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
