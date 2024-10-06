"""Urls module for cat_expo app."""

from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BreedListView
from .views import ByBreedListView
from .views import KittenViewSet
from .views import RatingViewSet

router = DefaultRouter()
router.register(r"kittens", KittenViewSet, basename="kitten")
router.register(r"ratings", RatingViewSet, basename="rating")

app_name = "cat_expo"

urlpatterns: list[path] = [
    path("", include(router.urls)),
    path("breeds/", BreedListView.as_view(), name="breeds-list"),
    path("breed/<int:breed_id>/", ByBreedListView.as_view(), name="kittens-by-breed"),
]
