from django.db import IntegrityError
from rest_framework import serializers

from .models import Animal
from .models import Breed
from .models import Color
from .models import Description
from .models import Nickname
from .models import Rating


class NicknameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nickname
        fields = ["nickname"]
        extra_kwargs = {
            "nickname": {"validators": []},
        }


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ["description"]


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ["breed"]
        extra_kwargs = {
            "breed": {"validators": []},
        }


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["color"]
        extra_kwargs = {
            "color": {"validators": []},
        }


class AnimalSerializer(serializers.ModelSerializer):
    nickname = NicknameSerializer()
    description = DescriptionSerializer()
    breed = BreedSerializer()
    color = ColorSerializer()

    class Meta:
        model = Animal
        fields = ["id", "nickname", "description", "breed", "color", "age", "user"]

    def create(self, validated_data):
        nickname_data = validated_data.pop("nickname")
        description_data = validated_data.pop("description")
        breed_data = validated_data.pop("breed")
        color_data = validated_data.pop("color")

        # Handle creation or fetching of existing records
        nickname, _ = Nickname.objects.get_or_create(**nickname_data)
        description, _ = Description.objects.get_or_create(**description_data)
        breed, _ = Breed.objects.get_or_create(**breed_data)
        color, _ = Color.objects.get_or_create(**color_data)

        try:
            animal = Animal.objects.create(
                nickname=nickname,
                description=description,
                breed=breed,
                color=color,
                **validated_data,
            )
        except IntegrityError as err:
            msg = f"User already added {nickname} previously"
            raise serializers.ValidationError(msg) from err

        return animal

    def update(self, instance, validated_data):
        nickname_data = validated_data.pop("nickname", None)
        description_data = validated_data.pop("description", None)
        breed_data = validated_data.pop("breed", None)
        color_data = validated_data.pop("color", None)

        if nickname_data:
            nickname, _ = Nickname.objects.update_or_create(**nickname_data)
            instance.nickname = nickname

        if description_data:
            description, _ = Description.objects.update_or_create(
                description=description_data.get("description")
            )
            instance.description = description

        if breed_data:
            breed, _ = Breed.objects.update_or_create(breed=breed_data.get("breed"))
            instance.breed = breed

        if color_data:
            color, _ = Color.objects.update_or_create(color=color_data.get("color"))
            instance.color = color

        # Update the rest of the fields
        instance.age = validated_data.get("age", instance.age)
        instance.user = validated_data.get("user", instance.user)
        try:
            instance.save()
        except IntegrityError as err:
            msg = f"User already added {instance.nickname} previously"
            raise serializers.ValidationError(msg) from err

        return instance


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["animal", "rating", "user"]
        extra_kwargs = {
            "user": {"read_only": True},  # User is taken from the request
        }

    def create(self, validated_data):
        rating, created = Rating.objects.update_or_create(
            user=self.context["request"].user,
            animal=validated_data["animal"],
            defaults={"rating": validated_data["rating"]},
        )
        return rating
