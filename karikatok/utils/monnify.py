import requests
from django.conf import settings
import logging
import base64
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from finance.models import Wallet
from accounts.models import User

# logger = logging.getLogger(__name__)

class MonnifyService:
    @staticmethod
    def get_auth_token():
        url = f"{settings.MONNIFY_BASE_URL}/api/v1/auth/login"
        credentials = f"{settings.MONNIFY_API_KEY}:{settings.MONNIFY_SECRET_KEY}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}"
        }
        print(encoded_credentials)
        print('heyyyyy')
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json().get("responseBody", {}).get("accessToken")
    get_auth_token()


    @staticmethod
    def create_account(account_reference, account_name, customer_name, customer_email, bvn, get_all_available_banks):
        token = MonnifyService.get_auth_token()
        url = f"{settings.MONNIFY_BASE_URL}/api/v2/bank-transfer/reserved-accounts"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "accountReference": account_reference,
            "accountName": account_name,
            "currencyCode": "NGN",
            "contractCode": settings.MONNIFY_CONTRACT_CODE,
            "customerEmail": customer_email,
            "customerName": customer_name,
            "bvn": bvn,
            "getAllAvailableBanks": get_all_available_banks
        }
        print(f"Payload being sent: {payload}")

        # logger.debug("Monnify Payload: %s", payload)
        # logger.debug("Headers: %s", headers)

        response = requests.post(url, json=payload, headers=headers)

        try:
            response.raise_for_status()
            return response.json().get("responseBody")
        except requests.exceptions.HTTPError as e:
            # logger.error("Monnify API Error: %s", response.text)
            raise Exception(f"Failed to create wallet: {response.text}")


    @csrf_exempt
    def monnify_webhook(request):
        if request.method == "POST":
            payload = json.loads(request.body)
            if payload.get("event") == "transactionSuccessful":
                account_reference = payload["accountReference"]
                amount_paid = float(payload["amountPaid"])

                # Find the user wallet by account reference
                user = User.objects.get(id=account_reference)
                wallet = Wallet.objects.get(user=user)
                wallet.balance += amount_paid
                wallet.save()

                return JsonResponse({"status": "success"}, status=200)

        return JsonResponse({"status": "ignored"}, status=400)


    def initialize_transaction(amount, account_reference):
        token = get_auth_token()
        url = f"{settings.MONNIFY_BASE_URL}/transactions/initialize"
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "amount": amount,
            "customerName": "Wallet Funding",
            "customerEmail": "example@example.com",
            "paymentReference": account_reference,
            "currencyCode": "NGN",
            "paymentDescription": "Wallet Funding",
            "incomeSplitConfig": [],
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
# response = MonnifyService.create_wallet(
#     wallet_reference="ref123456789",
#     wallet_name="Test Wallet",
#     customer_name="John Doe",
#     customer_email="john.doe@example.com",
#     bvn="12345678901",
#     bvn_date_of_birth="1990-01-01"
# )
# print(response)