from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('anotherprice_index.urls')),
    path('admin/', admin.site.urls),
]