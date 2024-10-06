from django.db import models

from wm_test.cat_expo.models import Color

from .models import BaseModelFieldTest
from .models import BaseModelTest


class BaseModel:
    model = Color


class TestModelColor(BaseModel, BaseModelTest):
    def test_tag_has_all_attributes(self, instance):
        assert hasattr(instance, "id")
        assert hasattr(instance, "color")


class TestFieldColor(BaseModel, BaseModelFieldTest):
    field_name = "color"
    field_type = models.CharField

    blank = False
    null = False
    unique = True
    max_length = 255
