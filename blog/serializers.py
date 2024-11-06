from rest_framework import serializers

from .models import Writer, Article


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ['user', 'is_editor', 'name']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id', 'created_at', 'title', 'content', 'status', 'written_by',
            'edited_by',
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    written_by = WriterSerializer(read_only=True)
    edited_by = WriterSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'created_at', 'title', 'content', 'status', 'written_by',
            'edited_by',
        ]


class ArticleStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['status', 'edited_by']
