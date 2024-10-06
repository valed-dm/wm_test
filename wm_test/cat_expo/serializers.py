"""Serializers module for cat_expo app."""

from typing import Any

from django.db import IntegrityError
from django.db import transaction
from rest_framework import serializers

from .models import Breed
from .models import Color
from .models import Description
from .models import Kitten
from .models import Nickname
from .models import Rating


class NicknameSerializer(serializers.ModelSerializer):
    """
    Serializer for the Nickname model. Handles serialization and deserialization
    of kitten nicknames, disabling the default uniqueness validator.
    """

    class Meta:
        model = Nickname
        fields = ["id", "nickname"]
        extra_kwargs = {
            "nickname": {"validators": []},
        }


class DescriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Description model. Handles serialization and deserialization
    of kitten descriptions.
    """

    class Meta:
        model = Description
        fields = ["id", "description"]


class BreedSerializer(serializers.ModelSerializer):
    """
    Serializer for the Breed model. Handles serialization and deserialization
    of kitten breeds, disabling the default uniqueness validator.
    """

    class Meta:
        model = Breed
        fields = ["id", "breed"]
        extra_kwargs = {
            "breed": {"validators": []},
        }


class ColorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Color model. Handles serialization and deserialization
    of kitten colors, disabling the default uniqueness validator.
    """

    class Meta:
        model = Color
        fields = ["id", "color"]
        extra_kwargs = {
            "color": {"validators": []},
        }


class KittenSerializer(serializers.ModelSerializer):
    """
    Serializer for the Kitten model. Handles serialization and deserialization
    of Kitten objects, including related fields like nickname, description, breed,
    and color.
    Supports the creation and update of related objects.
    """

    nickname = NicknameSerializer()
    description = DescriptionSerializer()
    breed = BreedSerializer()
    color = ColorSerializer()

    class Meta:
        model = Kitten
        fields = ["id", "nickname", "description", "breed", "color", "age", "user"]

    def create(self, validated_data: dict[str, Any]) -> Kitten:
        """
        Creates a new Kitten object along with related objects (nickname,
        description, breed, color). If the nickname already exists for the user,
        an IntegrityError is raised.
        Args:
            validated_data (dict): Validated data for creating the kitten and related
            objects.
        Returns:
            Kitten: The created Kitten instance.
        """
        # Extract and handle nested related data
        nickname_data = validated_data.pop("nickname")
        description_data = validated_data.pop("description")
        breed_data = validated_data.pop("breed")
        color_data = validated_data.pop("color")

        with transaction.atomic():
            # Handle creation or fetching of existing records
            nickname, _ = Nickname.objects.get_or_create(**nickname_data)
            description, _ = Description.objects.get_or_create(**description_data)
            breed, _ = Breed.objects.get_or_create(**breed_data)
            color, _ = Color.objects.get_or_create(**color_data)

            # Create the Kitten object
            try:
                kitten = Kitten.objects.create(
                    nickname=nickname,
                    description=description,
                    breed=breed,
                    color=color,
                    **validated_data,
                )
            except IntegrityError as err:
                msg = f"User already added kitten {nickname} previously"
                raise serializers.ValidationError(msg) from err

        return kitten

    def update(self, instance: Kitten, validated_data: dict[str, Any]) -> Kitten:
        """
        Updates an existing Kitten object and its related objects (nickname,
        description, breed, color).
        Args:
            instance (Kitten): The existing Kitten instance to update.
            validated_data (dict): Validated data for updating the kitten and related
            objects.
        Returns:
            Kitten: The updated Kitten instance.
        """
        nickname_data = validated_data.pop("nickname", {})
        description_data = validated_data.pop("description", {})
        breed_data = validated_data.pop("breed", {})
        color_data = validated_data.pop("color", {})

        if nickname_data:
            nickname, _ = Nickname.objects.select_for_update().update_or_create(
                **nickname_data
            )
            instance.nickname = nickname

        if description_data:
            description, _ = Description.objects.select_for_update().update_or_create(
                description=description_data.get("description")
            )
            instance.description = description

        if breed_data:
            breed, _ = Breed.objects.select_for_update().update_or_create(
                breed=breed_data.get("breed")
            )
            instance.breed = breed

        if color_data:
            color, _ = Color.objects.select_for_update().update_or_create(
                color=color_data.get("color")
            )
            instance.color = color

        # Update the rest of the fields
        instance.age = validated_data.get("age", instance.age)
        instance.user = validated_data.get("user", instance.user)

        try:
            instance.save()
        except IntegrityError as err:
            msg = f"User already added kitten {instance.nickname} previously"
            raise serializers.ValidationError(msg) from err

        return instance


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rating model. Handles serialization and deserialization
    of rating data for kittens.
    The user is automatically set based on the request context.
    """

    class Meta:
        model = Rating
        fields = ["kitten", "rating", "user"]
        extra_kwargs = {
            "user": {"read_only": True},  # User is taken from the request
        }

    def create(self, validated_data: dict[str, Any]) -> Rating:
        """
        Creates or updates a Rating object for a kitten. Ensures that a user can only
        rate a kitten once, updating the rating if it already exists.
        Args:
            validated_data (dict): Validated data for creating or updating the rating.
        Returns:
            Rating: The created or updated Rating instance.
        """
        with transaction.atomic():
            rating, _ = Rating.objects.select_for_update().update_or_create(
                user=self.context["request"].user,
                kitten=validated_data["kitten"],
                defaults={"rating": validated_data["rating"]},
            )
        return rating
