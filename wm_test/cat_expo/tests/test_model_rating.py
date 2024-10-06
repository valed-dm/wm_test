from django.contrib.auth import get_user_model
from django.db import models

from wm_test.cat_expo.models import Kitten
from wm_test.cat_expo.models import Rating

from .models import BaseModelTest
from .models import BaseTestFieldRelated


class BaseModel:
    model = Rating


class TestModelRating(BaseModel, BaseModelTest):
    def test_tag_has_all_attributes(self, instance):
        assert hasattr(instance, "id")
        assert hasattr(instance, "kitten")
        assert hasattr(instance, "rating")
        assert hasattr(instance, "user")


class TestFieldKitten(BaseModel, BaseTestFieldRelated):
    field_name = "kitten"
    field_type = models.ForeignKey
    related_model = Kitten
    on_delete = models.CASCADE

    db_index = True
    blank = False
    null = False
    unique = False


class TestFieldRating(BaseModel, BaseTestFieldRelated):
    field_name = "rating"
    field_type = models.PositiveSmallIntegerField

    blank = False
    null = False
    unique = False


class TestFieldUser(BaseModel, BaseTestFieldRelated):
    field_name = "user"
    field_type = models.ForeignKey
    related_model = get_user_model()
    on_delete = models.CASCADE

    db_index = True
    blank = False
    null = False
    unique = False
