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
        # Create the News instance
        news_instance = News.objects.create(**validated_data)

        # Handle tag creation or retrieval by name and associate with the news instance
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)  # Create or fetch tag
            tags.append(tag)

        # Associate the tags with the news instance (many-to-many relation)
        news_instance.tags.set(tags)
        return news_instance
