from django.shortcuts import render
from utils.monnify import get_monnify_token

# class 

# Create your views here.
#create an endpoint to get a status from the frontend
#I use it to query their api and see whether it works

#wallet table balance before balance after

# transaction table that shows h

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
from .models import Wallet
from rest_framework.permissions import IsAuthenticated

class FundWallet(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only logged-in users can fund their wallets.

    def post(self, request, *args, **kwargs):
        amount = request.data.get("amount")
        if not amount or float(amount) <= 0:
            return Response({"error": "Amount must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)

        # Use Monnify to initiate wallet funding
        monnify_url = "https://sandbox.monnify.com/api/v1/transaction/initialize"  # Adjust for production
        headers = {
            "Authorization": f"Bearer {settings.MONNIFY_API_KEY}",
            "Content-Type": "application/json"
        }
        transaction_data = {
            "amount": amount,
            "customerName": request.user.username,
            "customerEmail": request.user.email,
            "paymentReference": f"wallet_{request.user.id}_{amount}",
            "currencyCode": "NGN",
            "redirectUrl": "http://your-frontend-url.com/payment-completed"
        }

        response = requests.post(monnify_url, json=transaction_data, headers=headers)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)

        return Response({"error": "Failed to initialize transaction"}, status=status.HTTP_400_BAD_REQUEST)
