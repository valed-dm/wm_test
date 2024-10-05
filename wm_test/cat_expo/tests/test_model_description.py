from django.db import models

from wm_test.cat_expo.models import Description

from .models import BaseModelFieldTest
from .models import BaseModelTest


class BaseModel:
    model = Description


class TestModelDescription(BaseModel, BaseModelTest):
    def test_tag_has_all_attributes(self, instance):
        assert hasattr(instance, "id")
        assert hasattr(instance, "description")


class TestFieldDescription(BaseModel, BaseModelFieldTest):
    field_name = "description"
    field_type = models.TextField

    blank = False
    null = False
    unique = True
