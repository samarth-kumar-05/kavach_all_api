from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import requests

from  .models import PhoneNumber
from .serializers import PhoneNumberSerializer
from .helper import get_phone_data

# Create your views here.
class PhoneQuery(APIView):
    def get(self,request):
        try:
            data = int(request.data.get("phone_number"))
            print(data)

            if PhoneNumber.objects.filter(phone_number = data).exists():
                res = PhoneNumber.objects.get(phone_number = data)

                new_dict = {
                    "phone_number":res.phone_number,
                    "is_spam":"true",
                    "spam_marks":res.spam_mark
                }

                return Response(new_dict)
            else:
                print("Start")
                carrier = get_phone_data(data)

                if(not carrier):
                    print(carrier + " No Carrier Found")
                if(carrier):
                    new_dict = {
                        "phone_number":data,
                        "is_spam":"false",
                        "spam_marks":0
                    }
                    return Response(new_dict)
                elif not carrier:
                    new_data = {"phone_number":data,"spam_mark":1}
                    serializer = PhoneNumberSerializer(data=new_data)

                    if serializer.is_valid():
                        serializer.save()
                        new_dict = {
                            "phone_number":data,
                            "is_spam":"true",
                            "spam_marks":1
                        }

                        return Response(new_dict)
                    else:
                        return Response("Please Enter a Valid Number",status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Please Enter Valid Number",status = status.HTTP_400_BAD_REQUEST)
        
class SpamMark(APIView):
    def put(self,request):
        data = int(request.data.get("phone_number"))

        if PhoneNumber.objects.filter(phone_number=data).exists():
            print("Working start")
            header_data = PhoneNumber.objects.get(phone_number=data)

            spam_marks = header_data.spam_mark+1
            new_dict = {
                "phone_number":header_data.phone_number,
                "is_spam":"true",
                "spam_mark":spam_marks
            }
            serializer = PhoneNumberSerializer(header_data,data=new_dict)

            print("WOrking till serilizer")

            if(serializer.is_valid()):
                serializer.save()

                new_dict = {
                        "phone_number":header_data.phone_number,
                        "is_spam":"true",
                        "spam_marks":header_data.spam_mark
                }

                return Response(new_dict)
            else:
                return Response("Please Provide a valid Phone Number ", status=status.HTTP_400_BAD_REQUEST)
            
        else:
            data = {
                "phone_number" : data,
                "spam_mark":1
            }

            serializer = PhoneNumberSerializer(data=data)

            if serializer.is_valid():
                serializer.save()

                new_dict = {
                    "phone_number":data,
                    "is_spam":"true",
                    "spam_marks":1
                }

                return Response(new_dict)
            else:
                return Response("Please Provide a valid Phone Number ", status=status.HTTP_400_BAD_REQUEST)


class Test(APIView):
    def get(self,request):
        data = (
            ("GET","/phone/query"),
            ("PUT","/phone/flag_spam"),
        )
        return Response(data)




