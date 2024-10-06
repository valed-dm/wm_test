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
