from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'first_name', 'last_name', 'dob', 'username', 'address', 'phone_number']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            dob=validated_data['dob'],
            phone_number=validated_data['phone_number'],
            address=validated_data['address']
        )
        return user


    

#Login should be a six digit number   
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            raise serializers.ValidationError("Email and password are required")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        # Check if the password matches
        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid email or password")

        # Check if the user is active
        if not user.is_active:
            raise serializers.ValidationError("User is not active")

        # Add the user to the validated data
        data['user'] = user
        return data

#Proof of concep
#signup and login
#Automatic wallet creation
#Deposit into the wallet
# Webhook or trigger to let us know when money has been transferred
# Table for items and choices
# Status code for the kini should be completedafter it has been scanned, not ongoing