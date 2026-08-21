from rest_framework import serializers

from .models import Actor, Movie, Review


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "movie", "grade"]


class MovieListSerializer(serializers.ModelSerializer):
    average_grade = serializers.FloatField(read_only=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "average_grade"]


class MovieDetailSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    actor_ids = serializers.PrimaryKeyRelatedField(
        queryset=Actor.objects.all(), source="actors", many=True, write_only=True, required=False
    )
    average_grade = serializers.FloatField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "description", "actors", "actor_ids", "average_grade", "reviews"]