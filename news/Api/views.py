from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
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

        # Handle include keywords (union logic)
        raw_include = self.request.query_params.getlist('include')
        include_keywords = []
        for item in raw_include:
            include_keywords.extend([kw.strip() for kw in item.split(',') if kw.strip()])
        if include_keywords:
            include_q = Q()
            for kw in include_keywords:
                include_q |= Q(title__icontains=kw) | Q(content__icontains=kw)
            queryset = queryset.filter(include_q)

        # Handle exclude keywords (union logic)
        raw_exclude = self.request.query_params.getlist('exclude')
        exclude_keywords = []
        for item in raw_exclude:
            exclude_keywords.extend([kw.strip() for kw in item.split(',') if kw.strip()])
        if exclude_keywords:
            exclude_q = Q()
            for kw in exclude_keywords:
                exclude_q |= Q(title__icontains=kw) | Q(content__icontains=kw)
            queryset = queryset.exclude(exclude_q)

        return queryset
