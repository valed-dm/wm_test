from django.db.models import Avg
from django.db.models import Count
from rest_framework import generics
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Animal
from .models import Breed
from .models import Rating
from .serializers import AnimalSerializer
from .serializers import BreedSerializer
from .serializers import RatingSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the animal
        return obj.user == request.user


# Breeds list view
class BreedListView(generics.ListAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


# Animals filtered by breed
class ByBreedListView(generics.ListAPIView):
    serializer_class = AnimalSerializer

    def get_queryset(self):
        breed_id = self.kwargs["breed_id"]
        return Animal.objects.filter(breed_id=breed_id)


# CRUD endpoint
class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """
        Override perform_create to prevent users from rating their own animals.
        """
        animal = serializer.validated_data["animal"]
        if animal.user == self.request.user:
            msg = "You cannot rate your own animal."
            raise serializers.ValidationError(msg)

        serializer.save(user=self.request.user)

    # Custom action to get average rating and vote count
    @action(detail=True, methods=["get"], url_path="rating-info")
    def rating_info(self, request, pk=None):
        """
        Returns the average rating and the total number of votes for the given animal.
        Can be accessed via the URL /api/ratings/<animal_id>/rating-info/.
        """
        rating_instance = self.get_object()
        animal = rating_instance.animal

        ratings = Rating.objects.filter(animal=animal)

        # Get the average rating and total votes
        avg_rating = ratings.aggregate(Avg("rating"))["rating__avg"]
        vote_count = ratings.aggregate(Count("rating"))["rating__count"]

        return Response(
            {
                "animal": animal.id,
                "animal_name": animal.nickname.nickname,
                "animal_breed": animal.breed.breed,
                "animal_description": animal.description.description,
                "average_rating": avg_rating or 0,  # Default to 0 if no ratings
                "vote_count": vote_count or 0,  # Default to 0 if no votes
            }
        )
