from rest_framework import serializers
from users.models import Profile
from authentication.models import User
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "date_joined",
            "first_name",
            "last_name"
        ]
        read_only_fields = ["date_joined", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = [
            "bio",
            # "profile_img",
            "user"
        ]
    
    def update(self, instance, validated_data):
        user = validated_data.pop("user")
        first_name = user.get("first_name")
        last_name = user.get("last_name")
        username = user.get("username")
        if first_name is not None:
            if first_name == "":
                raise ValidationError([
                    {
                        "first_name": [
                            "can not be empty"
                        ]
                    }
                ])
            instance.user.first_name = first_name
        if last_name is not None:
            instance.user.last_name = last_name
        if username is not None and username != instance.user.username:
            instance.user.username = username

        instance.user.save()

        return super().update(instance, validated_data)