from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from finance.models import Wallet
from utils.monnify import MonnifyService
from django.db import transaction

from django.conf import settings

User = get_user_model()

class Signup(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
            serializer = SignupSerializer(data=request.data)
            
            if serializer.is_valid():
                try:
                    user = serializer.save()
                    return Response(
                        {
                            "message": "Signup successful",
                            "user": {
                                "id": user.id,
                                "username": user.username,
                                "email": user.email,
                            },
                        },
                        status=status.HTTP_201_CREATED,
                    )
                except Exception as e:
                    transaction.set_rollback(True)
                    return Response(
                        {"error": f"Signup failed: {str(e)}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    ) # This handles validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Login(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        print(f"Request data: {request.data}")  # Print incoming data
        if serializer.is_valid():
            print('is user?')
            user = serializer.validated_data['user']
            print('hi user')
            # Generate the token using simplejwt
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            print('hola')

            return Response(
                {
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        else: print('Serializer errors:', serializer.errors)  # Print the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateAccount(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        required_fields = ["accountReference", "accountName", 
            "customerName", "customerEmail", "bvn"]

        # Validate top-level required fields
        for field in required_fields:
            if field not in data:
                return Response(
                    {"error": f"{field} is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        account_reference = data.get("accountReference")
        account_name = data.get("accountName")
        customer_name = data.get("customerName")
        customer_email = data.get("customerEmail")
        bvn = data.get("bvn")
        get_all_available_banks = data.get("getAllAvailableBanks", True)  # Default to True

        try:
            account = MonnifyService.create_account(
                account_reference=account_reference,
                account_name=account_name,
                customer_name=customer_name,
                customer_email=customer_email,
                bvn=bvn,
                get_all_available_banks=get_all_available_banks
            )
            return Response(account, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)