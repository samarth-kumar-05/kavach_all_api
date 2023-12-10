from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import requests

from .models import WalletAddress
from .serializers import WalletAddressSerializer

class WalletQuery(APIView):

    def get(self,request):

        try:
            walletaddress = request.data.get("wallet_address")

            if WalletAddress.objects.filter(address = walletaddress).exists():
                data = WalletAddress.objects.get(address = walletaddress)

                new_dict = {
                    "wallet_address":data.address,
                    "spam_marks":data.spam_marks
                }

                return Response(new_dict)

            else:
                new_dict = {
                    "wallet_address":walletaddress,
                    "spam_marks":0
                }
                
                return Response(new_dict)
            
        except:
            return Response("Please send a valid address")
        
class SpamMark(APIView):
    def put(self,request):
        wallet_address = request.data.get("wallet_address")

        if WalletAddress.objects.filter(address = wallet_address).exists():
                wallet_data = WalletAddress.objects.get(address = wallet_address)

                spam_mark = wallet_data.spam_marks+1

                new_dict = {
                    "wallet_address":wallet_data.address,
                    "spam_marks":spam_mark
                }

                serializer = WalletAddressSerializer(wallet_data,data=new_dict)

                if(serializer.is_valid()):
                    serializer.save()

                    new_dict =  new_dict = {
                        "wallet_address":wallet_data.address,
                        "spam_marks":spam_mark
                    }

                    return Response(new_dict)
        else:
            new_dict =  new_dict = {
                "wallet_address":wallet_data.address,
                "spam_marks":1
            }

            serializer = WalletAddressSerializer(data = new_dict)
            if serializer.is_valid():
                serializer.save()

                return Response(new_dict)
        

# Create your views here.
