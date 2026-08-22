from django.db.models import Avg
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Actor, Movie, Review
from .serializers import (
    ActorSerializer,
    MovieDetailSerializer,
    MovieListSerializer,
    ReviewSerializer,
)

# Create your views here.
class MoviePagination(PageNumberPagination):
    page_size = 5
    
class MovieViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    pagination_class = MoviePagination
    
    def get_queryset(self):
        return Movie.objects.annotate(average_grade=Avg("reviews__grade")).order_by("title")
    
    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        return MovieDetailSerializer
    
class ActorViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    
class ReviewViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer