from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re
import json

import requests

from .models import SMSHeaders
from sms.serializers import SMSHeaderSerializer

# Create your views here.
class HeaderQuery(APIView):
    def get(self,request,**kwargs):
        try:
            message = request.data.get("message")

            print(message)

            # regex=r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
            # matches = re.findall(regex, message)
            # print(matches)

            # url_context = {}
            # i=0
            # for url in matches:
            #     result = requests.post("https://kavach-api.onrender.com/url",json= {
            #         "url":url
            #     })
            #     new = {
            #         "name":url,
            #         "result":json.loads(result.text)
            #     }
            #     url_context.update({i:new})
            #     i+=1

            # print(url_context)
            print("printing header data")
            header = self.kwargs["header"] 
            print(header)
            if SMSHeaders.objects.filter(name = header).exists():
                header_details = SMSHeaders.objects.get(name = header)
                num_spams = header_details.spam_mark

                new_dict = {
                    "name":header,
                    "is_spam": True,
                    "number_of_spam_marks" : num_spams
                }

                # new_dict.update({"links":url_context})

                return Response(new_dict)
            else:

                print("ELSE BLOCK STARTED")

                message = request.data.get("message")

                print(message)

                url = "https://kavach-api.onrender.com/message"
                context = {
                    "message":message
                }

                print("requesting data")

                data = requests.post(url=url,json=context)
                

                print("request send")
                print(data)

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
                    # new_dict.update({"links":url_context})

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

                    # new_dict.update({"links":url_context})

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

