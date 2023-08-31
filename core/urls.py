from django.contrib import admin
from django.urls import include, path

handler500 = "core.http.exception_handler.server_error"
handler404 = "core.http.exception_handler.not_found"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.authentication.urls"), name="authentication"),
]
