from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Animal
from .models import Breed
from .serializers import AnimalSerializer
from .serializers import BreedSerializer


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
