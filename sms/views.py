from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import requests

from .models import SMSHeaders
from sms.serializers import SMSHeaderSerializer

# Create your views here.
class HeaderQuery(APIView):
    def get(self,request,**kwargs):
        try:
            header = self.kwargs["header"] 
            if SMSHeaders.objects.filter(name = header).exists():
                header_details = SMSHeaders.objects.get(name = header)
                num_spams = header_details.spam_mark

                new_dict = {
                    "name":header,
                    "is_spam": True,
                    "number_of_spam_marks" : num_spams
                }

                return Response(new_dict)
            else:

                message = request.data.get("message")

                url = "https://kavach-api.onrender.com/message"
                context = {
                    "message":message
                }

                print("requesting data")

                data = requests.post(url=url,json=context)

                print("request send")

                data_json = data.json()

                print(data_json)

                is_message_spam = data_json['result']

                print(is_message_spam)

                if(is_message_spam == 0):
                    new_dict = {
                        "name":header,
                        "is_spam" : False,
                        "number_of_spam_marks" : 0
                    }

                    return Response(new_dict)
                
                else:
                    
                    header_data = {"name":header,"spam_mark":1}

                    serializer = SMSHeaderSerializer(data=header_data)

                    if serializer.is_valid():
                        serializer.save()

                    new_dict = {
                        "name":header,
                        "is_spam" : True,
                        "number_of_spam_marks" : 1
                    }

                return Response(new_dict)
            
        except:
            return Response("Please Provide a valid SMS header ", status=status.HTTP_400_BAD_REQUEST)
        
class SpamMark(APIView):
    def put(self,request,**kwargs):
        header = self.kwargs["header"]

        if SMSHeaders.objects.filter(name=header).exists():
            header_data = SMSHeaders.objects.get(name=header)

            spam_marks = header_data.spam_mark+1
            new_dict = {
                "name":header,
                "spam_mark":spam_marks
            }

            serializer = SMSHeaderSerializer(header_data,data=new_dict)

            if(serializer.is_valid()):
                serializer.save()

                res = {
                    "name":header,
                    "is_spam":True,
                    "number_of_spam_marks":spam_marks
                }

                return Response(res)
            
        else:
            data = {
                "name" : header,
                "spam_mark":1
            }

            serializer = SMSHeaderSerializer(data=data)

            if serializer.is_valid():
                serializer.save()

                new_dict = {
                    "name":header,
                    "is_spam" : True,
                    "number_of_spam_marks" : 1
                }

                return Response(new_dict)
            else:
                return Response("Please Provide a valid SMS header ", status=status.HTTP_400_BAD_REQUEST)


class Test(APIView):
    def get(self,request):
        data = (
            ("GET","/sms_header/header"),
            ("PUT","/sms_header/flag_spam/header"),
        )
        return Response(data)

