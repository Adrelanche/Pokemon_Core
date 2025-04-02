from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FavoritePokemon


class FavoritePokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritePokemon
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    password = serializers.CharField(min_length=8, max_length=128, write_only=True)
    username = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("E-mail is already registered. Please, try again.")
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already registered. Please, try again.")
        return value

    def validate_password(self, value): 
        if len(value) < 8:
            raise serializers.ValidationError("Password must have at least 8 characters.")
        return value

    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user
