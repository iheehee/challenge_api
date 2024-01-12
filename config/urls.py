from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

URI = "api"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{URI}/challenge/", include("challenge.urls")),
    path(f"{URI}/user/", include("user.urls")),
    path(f"{URI}/auth/", include("access.urls")),
] + static(URI + settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
