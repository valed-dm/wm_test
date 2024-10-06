from django.db import models

from wm_test.cat_expo.models import Breed

from .models import BaseModelFieldTest
from .models import BaseModelTest


class BaseModel:
    model = Breed


class TestModelBreed(BaseModel, BaseModelTest):
    def test_tag_has_all_attributes(self, instance):
        assert hasattr(instance, "id")
        assert hasattr(instance, "breed")


class TestFieldBreed(BaseModel, BaseModelFieldTest):
    field_name = "breed"
    field_type = models.CharField

    blank = False
    null = False
    unique = True
    max_length = 255
