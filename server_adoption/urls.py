from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("files/", include("db_file_storage.urls")),
    path("", include("shelter.urls")),
]
