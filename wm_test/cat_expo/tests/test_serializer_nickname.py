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
