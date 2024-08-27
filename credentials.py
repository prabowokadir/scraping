import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    "https://www.googleapis.com/auth/bigquery",
    "https://www.googleapis.com/auth/cloud-platform"
]

def get_credentials(
        client_secrets_file="/Users/prabowo.kadir/Desktop/client_secret_522378535070-7n86ogodaj9jgitmrcd9rkqeomogqfff.apps.googleusercontent.com.json",
        token_file="token.pickle")
    creds = None
    