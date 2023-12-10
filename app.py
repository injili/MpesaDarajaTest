from flask import Flask, request
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64

app = Flask(__name__)

CONSUMER_KEY = "QpHMdxNNbxbYMJBNuq1KZFi1YDcGXZLN"
CONSUMER_SECRET = "9avA0ki8hFkR32Hh"
BUSINESS_PAYBILL = "174379"  # Replace with your actual business paybill number
PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"  # Replace with your actual passkey
CALLBACK_ENDPOINT = "https://d21e-105-49-221-137.ngrok-free.app/lnmo-callback"

# Welcome route
@app.route('/')
def home():
    return 'Hello World!'

# Initiate M-PESA Express request
# /pay?phone=&amount=1
@app.route('/pay')
def mpesa_express():
    amount = request.args.get('amount')
    phone = request.args.get('phone')

    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    access_token = get_access_token()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode((BUSINESS_PAYBILL + PASSKEY + timestamp).encode('utf-8')).decode('utf-8')

    headers = {
        "Authorization": "Bearer %s" % access_token,
    }
    data = {
        "BusinessShortCode": BUSINESS_PAYBILL,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "PartyA": phone,
        "PartyB": BUSINESS_PAYBILL,
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_ENDPOINT,
        "AccountReference": "TestPay",
        "TransactionDesc": "HelloTest",
        "Amount": amount
    }

    print("Request Data:", data)
    response = requests.post(endpoint, json=data, headers=headers)
    print("Response Data:", response.json())
    
    return response.json()

# Consume M-PESA Express callback
@app.route('/lnmo-callback', methods=["POST"])
def lnmo_callback():
    data = request.get_json()
    print(data)
    return "ok"

# Get access token (authorization api)
def get_access_token():
    endpoint = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(endpoint, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    data = response.json()
    return data['access_token']

if __name__ == '__main__':
    app.run(port=8811)
