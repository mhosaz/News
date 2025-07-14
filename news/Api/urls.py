from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet

router = DefaultRouter()
router.register('news', NewsViewSet, basename='news')
app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]
