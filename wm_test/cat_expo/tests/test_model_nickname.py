from django.db import models

from wm_test.cat_expo.models import Nickname

from .models import BaseModelFieldTest
from .models import BaseModelTest


class BaseModel:
    model = Nickname


class TestModelNickname(BaseModel, BaseModelTest):
    def test_tag_has_all_attributes(self, instance):
        assert hasattr(instance, "id")
        assert hasattr(instance, "nickname")


class TestFieldNickname(BaseModel, BaseModelFieldTest):
    field_name = "nickname"
    field_type = models.CharField

    blank = False
    null = False
    unique = True
    max_length = 255
