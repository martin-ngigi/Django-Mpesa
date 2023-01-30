from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from django.http import HttpResponse
from django.http import JsonResponse
import requests
from django.shortcuts import render, redirect
from requests.auth import HTTPBasicAuth
import json
from .models import *
from time import sleep, perf_counter
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from project import settings
import time
from time import sleep
from django.core.mail import send_mail



def getAccessToken(request):
    consumer_key = 'i0ddLaATcR2ewejbKWGvLap9FXGMp9dP'
    consumer_secret = 'Azleg1Si8MVkBKJI'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)


@csrf_exempt
def lipa_na_mpesa_online(request):
    if request.method == 'POST':
        body_unicode = request.POST  # request.body.decode('utf-8')
        #body = json.loads(body_unicode)
        print(body_unicode)
        global payinfo
        payinfo = body_unicode
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        # request = {
        #     "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        #     "Password": LipanaMpesaPpassword.decode_password,
        #     "Timestamp": LipanaMpesaPpassword.lipa_time,
        #     "TransactionType": "CustomerPayBillOnline",
        #     "Amount": int(float(body_unicode['total'])),
        #     "PartyA": body_unicode['phone'],
        #     "PartyB": LipanaMpesaPpassword.Business_short_code,
        #     "PhoneNumber": body_unicode['phone'],
        #     "CallBackURL": "https://2011-105-163-2-19.in.ngrok.io/callback/",
        #     "AccountReference": "WMS for %s" % body_unicode['invoice_id'],
        #     "TransactionDesc": "WMS for %s" % body_unicode['invoice_id']
        # }

        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,
            "PartyA": 254797292290,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": 254797292290,
            "CallBackURL": "https://7f1b-105-163-158-216.in.ngrok.io/callback/",
            "AccountReference": "MartinLMTD",
            "TransactionDesc": "SW Payment"
        }


        response = requests.post(api_url, json=request, headers=headers)
        print("The response is:",response)
        return HttpResponse({"CallBack Sent successfully! ":response})
        
    #else
    print("Empty response.........................................................................")

    #sleep(15)
    #return redirect("display")


@csrf_exempt
def MpesaCallBack(request):
    message='Message is :'
    try:
        data = request.body.decode('utf-8')
        #print("callback sent:"+str(data))
        mpesa_payment = json.loads(data)
        print(mpesa_payment)
        #print(mpesa_payment)
        result = 0
        if result == mpesa_payment['Body']['stkCallback']['ResultCode']: # if result = 0
            message = "Payment Made Successfully."
            print(message)         
        else:
            message = "Request Failed!\nPayment cancelled by user!"
            print(message)
        return message
    except Exception as e:
        print(e)

