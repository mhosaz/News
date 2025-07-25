from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet

router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
app_name = 'Api'
urlpatterns = router.urls
