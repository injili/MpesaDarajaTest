from flask import Flask, request
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64

app = Flask(__name__)
my_endpoint = "https://eee8-105-161-77-221.ngrok-free.app"

# welcome route
@app.route('/')
def home():
    return 'Hello World!'

# Initiate M-PESA Express request
# /pay?phone=&amount=1
@app.route('/pay')
def MpesaExpress():
    amount = request.args.get('amount')
    phone = request.args.get('phone')

    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    access_token = getAccesstoken()

    business_paybill = "174379"  # Replace with your actual business paybill number
    lipa_na_mpesa_passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"  # Replace with your actual passkey

    Timestamp = datetime.now()
    times = Timestamp.strftime("%Y%m%d%H%M%S")
    password = base64.b64encode((business_paybill + lipa_na_mpesa_passkey + times).encode('utf-8')).decode('utf-8')

 

    headers = {
        "Authorization": "Bearer %s" % access_token,
    }
    data = {
        "BusinessShortCode": business_paybill,
        "Password": password,
        "Timestamp": times,
        "TransactionType": "CustomerPayBillOnline",
        "PartyA": phone,  # Customer's phone number
        "PartyB": business_paybill,
        "PhoneNumber": business_paybill,  # Payee's Lipa Na M-Pesa PayBill number
        "CallBackURL": my_endpoint + "/lnmo-callback",
        "AccountReference": "TestPay",
        "TransactionDesc": "HelloTest",
        "Amount": amount
    }

    print("Request Data:", data)
    res = requests.post(endpoint, json=data, headers=headers)
    print("Response Data:", res.json())
    
    return res.json()

# consume M-PESA Express callback
@app.route('/lnmo-callback', methods=["POST"])
def incoming():
    data = request.get_json()
    print(data)
    return "ok"

# get access token (authorization api)
def getAccesstoken():
    consumer_key = "QpHMdxNNbxbYMJBNuq1KZFi1YDcGXZLN"
    consumer_secret = "9avA0ki8hFkR32Hh"
    endpoint = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    r = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = r.json()
    return data['access_token']

if __name__ == '__main__':
    app.run(port=8811)
