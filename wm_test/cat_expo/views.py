"""Viewset module for cat_expo app."""

from typing import Any

from django.db.models import Avg
from django.db.models import Count
from django.db.models import QuerySet
from rest_framework import generics
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from .models import Breed
from .models import Kitten
from .models import Rating
from .serializers import BreedSerializer
from .serializers import KittenSerializer
from .serializers import RatingSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission that only allows the owner of a kitten object
    to modify or delete it. All users have read-only access.
    """

    def has_object_permission(self, request: Request, view: Any, obj: Any) -> bool:
        """
        Check if the requesting user has permission to modify the object.
        Args:
            request (Request): The current request object.
            view (Any): The view being accessed.
            obj (Any): The object being accessed.
        Returns:
            bool: True if the request is a safe method or if the user owns the object;
            False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class BreedListView(generics.ListAPIView):
    """
    API view to retrieve the list of all available breeds.
    """

    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class ByBreedListView(generics.ListAPIView):
    """
    API view to retrieve kittens filtered by breed.
    """

    serializer_class = KittenSerializer

    def get_queryset(self) -> QuerySet:
        """
        Retrieve the queryset of kittens based on breed_id provided in the URL.
        Returns:
            QuerySet: Queryset of kittens filtered by breed.
        """
        breed_id = self.kwargs["breed_id"]
        return Kitten.objects.filter(breed_id=breed_id)


class KittenViewSet(viewsets.ModelViewSet):
    """
    A viewset to handle CRUD operations for Kitten objects.
    Methods:
        - list: Retrieve a list of all kittens.
        - retrieve: Get details of a specific kitten.
        - create: Create a new kitten. The current user is set as the owner.
        - update: Update an existing kitten. Only the owner can perform this action.
        - partial_update: Partially update an existing kitten. Only the owner can
          perform this action.
        - destroy: Delete a kitten. Only the owner can perform this action.
    """

    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer: BaseSerializer) -> None:
        """
        Save the Kitten object with the current authenticated user as the owner.
        Args:
            serializer (BaseSerializer): The serializer instance.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer: BaseSerializer) -> None:
        """
        Update the Kitten object with the current authenticated user as the owner.
        Args:
            serializer (BaseSerializer): The serializer instance.
        """
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance: Kitten) -> None:
        """
        Delete the specified Kitten object.
        Args:
            instance (Kitten): The Kitten instance to delete.
        """
        instance.delete()


class RatingViewSet(viewsets.ModelViewSet):
    """
    A viewset to handle CRUD operations for Rating objects.
    Allows users to rate kittens, but prevents users from rating their own kittens.
    Methods:
        - list: Retrieve a list of all ratings.
        - retrieve: Get details of a specific rating.
        - create: Create a new rating. Users cannot rate their own kittens.
        - update: Update an existing rating. Only the rating's owner can perform
          this action.
        - partial_update: Partially update an existing rating. Only the owner can
          perform this action.
        - destroy: Delete a rating. Only the owner can perform this action.
        - rating_info (custom action): Retrieve the average rating and vote count for a
          specific kitten.
    """

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer: BaseSerializer) -> None:
        """
        Prevent users from rating their own kittens, and save the Rating object.
        Args:
            serializer (BaseSerializer): The serializer instance.
        Raises:
            ValidationError: If the user attempts to rate their own kitten.
        """
        kitten = serializer.validated_data["kitten"]
        if kitten.user == self.request.user:
            msg = "You cannot rate your own kitten."
            raise serializers.ValidationError(msg)

        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"], url_path="rating-info")
    def rating_info(self, request: Request, pk: str | None = None) -> Response:
        """
        Retrieve the average rating and vote count for a specific kitten.
        Args:
            request (Request): The current request object.
            pk (str): The primary key of the Rating object being accessed.
        Returns:
            Response: A response containing the average rating
            and vote count for the kitten: /api/ratings/<kitten_id>/rating-info/.
        """
        rating_instance = self.get_object()
        kitten = rating_instance.kitten

        ratings = Rating.objects.filter(kitten=kitten)

        # Get the average rating and total votes
        avg_rating = ratings.aggregate(Avg("rating"))["rating__avg"]
        vote_count = ratings.aggregate(Count("rating"))["rating__count"]

        return Response(
            {
                "kitten": kitten.id,
                "kitten_name": kitten.nickname.nickname,
                "kitten_breed": kitten.breed.breed,
                "kitten_description": kitten.description.description,
                "average_rating": avg_rating or 0,
                "vote_count": vote_count or 0,
            }
        )
