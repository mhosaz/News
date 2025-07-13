from django.urls import path
from . import views
app_name = 'api'
urlpatterns = [
    path('news/', views.NewsListAPIView.as_view(), name='news_list'),
]