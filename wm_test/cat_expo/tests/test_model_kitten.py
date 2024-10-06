from django.contrib.auth import get_user_model
from django.db import models

from wm_test.cat_expo.models import Breed
from wm_test.cat_expo.models import Color
from wm_test.cat_expo.models import Description
from wm_test.cat_expo.models import Kitten
from wm_test.cat_expo.models import Nickname

from .models import BaseModelTest
from .models import BaseTestFieldRelated


class BaseModel:
    model = Kitten


class TestModelKitten(BaseModel, BaseModelTest):
    def test_tag_has_all_attributes(self, instance):
        assert hasattr(instance, "id")
        assert hasattr(instance, "nickname")
        assert hasattr(instance, "description")
        assert hasattr(instance, "breed")
        assert hasattr(instance, "color")
        assert hasattr(instance, "age")
        assert hasattr(instance, "user")


class TestFieldNickname(BaseModel, BaseTestFieldRelated):
    field_name = "nickname"
    field_type = models.ForeignKey
    related_model = Nickname
    on_delete = models.CASCADE

    db_index = True
    blank = False
    null = False
    unique = False


class TestFieldDescription(BaseModel, BaseTestFieldRelated):
    field_name = "description"
    field_type = models.OneToOneField
    related_model = Description
    on_delete = models.CASCADE

    db_index = True
    blank = False
    null = False
    unique = True


class TestFieldBreed(BaseModel, BaseTestFieldRelated):
    field_name = "breed"
    field_type = models.ForeignKey
    related_model = Breed
    on_delete = models.CASCADE

    db_index = True
    blank = False
    null = False
    unique = False


class TestFieldColor(BaseModel, BaseTestFieldRelated):
    field_name = "color"
    field_type = models.ForeignKey
    related_model = Color
    on_delete = models.CASCADE

    db_index = True
    blank = False
    null = False
    unique = False


class TestFieldAge(BaseModel, BaseTestFieldRelated):
    field_name = "age"
    field_type = models.PositiveIntegerField

    blank = True
    null = True
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
