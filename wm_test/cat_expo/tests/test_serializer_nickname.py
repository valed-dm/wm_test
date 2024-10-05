from wm_test.cat_expo.models import Nickname
from wm_test.cat_expo.serializers import NicknameSerializer


def test_nickname_serializer_deserialization():
    # Simulate raw data input (what you'd receive from an API request)
    data = {"nickname": "Whiskers"}

    # Deserialize the input data into a model instance
    serializer = NicknameSerializer(data=data)

    assert serializer.is_valid(), serializer.errors

    # Save the new instance from deserialized data
    nickname_instance = serializer.save()
    assert nickname_instance.nickname == "Whiskers"


def test_nickname_serializer_serialization():
    # Create an instance of Nickname
    nickname_instance = Nickname.objects.create(nickname="Tommy")

    # Serialize the instance
    serializer = NicknameSerializer(nickname_instance)

    # Check if the data is serialized correctly
    expected_data = {
        "id": nickname_instance.id,
        "nickname": "Tommy",
    }
    assert serializer.data == expected_data


def test_nickname_serializer_unique():
    # Create an initial nickname
    initial_data = {"nickname": "Whiskers"}
    serializer = NicknameSerializer(data=initial_data)
    assert serializer.is_valid(), serializer.errors
    _ = serializer.save()

    # Now try to create a duplicate nickname
    duplicate_data = {"nickname": "Whiskers"}
    serializer = NicknameSerializer(data=duplicate_data)

    # Validate that the serializer does not allow duplicates
    assert not serializer.is_valid()
    assert "nickname" in serializer.errors
    assert serializer.errors["nickname"] == ["This nickname is already taken."]
