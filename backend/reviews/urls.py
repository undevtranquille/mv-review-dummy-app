from rest_framework.routers import DefaultRouter
from .views import ActorViewSet, MovieViewSet, ReviewViewSet

router = DefaultRouter()
router.register("movies", MovieViewSet, basename="movie")
router.register("actors", ActorViewSet, basename="actor")
router.register("reviews", ReviewViewSet, basename="review")

urlpatterns = router.urls