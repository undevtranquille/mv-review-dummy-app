from django.shortcuts import render
from django.db.models import Avg
from rest_framework import viewsets
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
    
class MovieViewSet(viewsets.ModelViewSet):
    pagination_class = MoviePagination
    
    def get_queryset(self):
        return Movie.objects.annotate(average_grade=Avg("reviews__grade"))
    
    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        return MovieDetailSerializer
    
class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer