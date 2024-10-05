from wm_test.cat_expo.models import Description
from wm_test.cat_expo.serializers import DescriptionSerializer


def test_description_serializer_deserialization():
    # Simulate raw data input (what you'd receive from an API request)
    data = {"description": "A thick, luxurious coat is a quality of the Persian cat."}

    # Deserialize the input data into a model instance
    serializer = DescriptionSerializer(data=data)

    assert serializer.is_valid(), serializer.errors

    # Save the new instance from deserialized data
    description_instance = serializer.save()
    assert description_instance.description == (
        "A thick, luxurious coat is a quality of the Persian cat."
    )


def test_description_serializer_serialization():
    # Create an instance of Description
    description_instance = Description.objects.create(
        description="Persian cats bring joy to families because of their loving."
    )

    # Serialize the instance
    serializer = DescriptionSerializer(description_instance)

    # Check if the data is serialized correctly
    expected_data = {
        "id": description_instance.id,
        "description": "Persian cats bring joy to families because of their loving.",
    }
    assert serializer.data == expected_data


def test_description_serializer_unique():
    # Create an initial description
    initial_data = {"description": "Personality and Temperament"}
    serializer = DescriptionSerializer(data=initial_data)
    assert serializer.is_valid(), serializer.errors
    _ = serializer.save()

    # Now try to create a duplicate description
    duplicate_data = {"description": "Personality and Temperament"}
    serializer = DescriptionSerializer(data=duplicate_data)

    # Validate that the serializer does not allow duplicates
    assert not serializer.is_valid()
    assert "description" in serializer.errors
    assert serializer.errors["description"] == ["This description is already taken."]
