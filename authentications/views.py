from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from jwcrypto import jwt
import jwt


def login_user():
    # Build the URL authorization to Microsoft Login
    authorization_url = (
        f"{settings.URL_MICROSOFT_LOGIN}{settings.TENANT_ID}/oauth2/v2.0/authorize"
    )
    client_id = settings.CLIENT_ID
    redirect_uri = f"{settings.URL_DEVELOP}/api/oauth2/callback"
    scope = "openid profile email"
    state = "L2FjY291bnRzL3Byb2ZpbGUv"  # Can be generated random

    # Using select_account prompt
    authorization_url += settings.AUTHORIZATION_URL_PROMPT_SELECT_ACCOUNT.format(
        client_id, redirect_uri, scope, state
    )

    # Redirect to the user URL authorization
    return redirect(authorization_url)


def oauth2_callback_view(request):
    authorization_code = request.GET.get("code")

    if authorization_code:
        # Perform the token exchange with your OAuth2 provider
        # Replace the following placeholders with your actual values
        token_endpoint = (
            f"{settings.URL_MICROSOFT_LOGIN}{settings.TENANT_ID}/oauth2/v2.0/token"
        )
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET
        redirect_uri = f"{settings.URL_DEVELOP}/api/oauth2/callback"

        payload = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        }

        response = requests.post(token_endpoint, data=payload)
        response_data = response.json()

        # Extract and handle the access token
        access_token = response_data.get("access_token")

        # Do something with the access token, e.g., store it in the session
        request.session["access_token"] = access_token

        # Redirect to a success URL or return a response as needed
        return redirect("/api/test/")
    else:
        return HttpResponse("Authorization code not provided")


class TestView(APIView):
    def get(self, request):
        # Retrieve the access token from the session
        access_token = request.session.get("access_token")
        if not access_token:
            return Response(
                "Access token not found in the session",
                status=status.HTTP_400_BAD_REQUEST,
            )

        decode_data = decode_token_without_secret(access_token)
        # Your code to handle the access token and other details
        if decode_data:
            content = {
                "message": "Hello, World!",
                "access_token": access_token,
                "user information": decode_data,
            }
            return Response(content)
        else:
            content = {"message": "Error to decode token"}
            return Response(content)


def decode_token_without_secret(token):
    try:
        decoded_payload = jwt.decode(token, options={"verify_signature": False})
        return decoded_payload
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Error to decode token: {e}")
        return None
