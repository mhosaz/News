from rest_framework import serializers
from .models import News, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class NewsSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True  # This will accept tag names (strings) as input
    )

    class Meta:
        model = News
        fields = ['title', 'content', 'source', 'tags']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        source = validated_data.get('source')

        # Check if news with the same source already exists
        # You might want to add more fields to check for uniqueness (like title, published_date, etc.)
        news_instance, created = News.objects.get_or_create(
            source=source,
            defaults=validated_data
        )

        # If the news already existed, we still want to update its tags
        if not created:
            # Update other fields if needed
            for attr, value in validated_data.items():
                setattr(news_instance, attr, value)
            news_instance.save()

        # Handle tag creation or retrieval by name and associate with the news instance
        tags = []
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)

        # Associate the tags with the news instance
        news_instance.tags.set(tags)

        return news_instance
