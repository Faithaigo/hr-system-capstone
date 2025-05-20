from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id','user','department','role','position','phone','address','profile_image']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile