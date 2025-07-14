from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('news/', include('Api.urls', namespace='api')),
    path('admin/', admin.site.urls),
]