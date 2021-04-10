from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        allow_null=True,
        queryset=Genre.objects.all()
    )

    category = serializers.SlugRelatedField(
        slug_field='slug',
        allow_null=True,
        queryset=Category.objects.all()
    )
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = [
            'id', 'name', 'year',
            'description', 'genre', 'category', 'rating'
        ]
        read_only_fields = ['rating']


class TitleReadSerializer(TitleSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    score = serializers.IntegerField(max_value=10, min_value=1)

    def validate(self, data):
        title = self.context.get('title')
        request = self.context.get('request')
        if (
            Review.objects.filter(
                author=request.user, title=title).exists() and
            request.method != 'PATCH'
        ):
            raise serializers.ValidationError('Оценка уже выставлена')
        return data

    class Meta:
        model = Review
        unique_together = ['title', 'author']
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        read_only_fields = ['title']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']
        read_only_fields = ['review']
