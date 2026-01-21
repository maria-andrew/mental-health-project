from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return redirect("login")   # redirect to accounts login


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),

    # include each app ONCE
    path("", include("accounts.urls")),
    path("tests/", include("tests.urls")),
    path("doctors/", include("doctors.urls")),
]

# media files (images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
