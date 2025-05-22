from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the built-in Django User model.

    Fields:
        - username
        - email
        - first_name
        - last_name
        - password (write-only for security)

    Handles creating and updating user instances, including securely
    setting the password.
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create and return a new user with an encrypted password.
        Uses `create_user()` which automatically handles password hashing.
        """
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """
        Update an existing user instance.
        If a password is provided, it is set securely using `set_password`.
        Other fields are updated directly.
        """
        password = validated_data.pop('password', None)

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.

    Includes a nested UserSerializer to handle user account creation
    or updates alongside the profile.
    """

    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'department', 'role', 'position', 'phone', 'address', 'profile_image']

    def create(self, validated_data):
        """
        Create a new User and UserProfile.

        Extracts user data from the nested serializer, creates the User,
        then creates the profile associated with that user.
        """
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        """
        Update an existing UserProfile and nested User.

        Handles both profile field updates and nested user field updates.
        Uses `partial=True` to allow partial updates.
        """
        user_data = validated_data.pop('user', {})

        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        instance.department = validated_data.get('department', instance.department)
        instance.role = validated_data.get('role', instance.role)
        instance.position = validated_data.get('position', instance.position)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.save()

        return instance
