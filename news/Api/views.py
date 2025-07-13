from rest_framework import generics
from .models import News
from .serializers import NewsSerializer
from django.db.models import Q

class NewsListAPIView(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = News.objects.all()

        # Filter by tag
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__name=tag)

        # Filter by keywords (must be present)
        include_keywords = self.request.query_params.getlist('include')
        for kw in include_keywords:
            queryset = queryset.filter(
                Q(title__icontains=kw) | Q(content__icontains=kw)
            )

        # Filter by keywords (must NOT be present)
        exclude_keywords = self.request.query_params.getlist('exclude')
        for kw in exclude_keywords:
            queryset = queryset.exclude(
                Q(title__icontains=kw) | Q(content__icontains=kw)
            )

        return queryset
