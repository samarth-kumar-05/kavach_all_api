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
    def get(self,request,**kwargs):
        try:
            data = self.kwargs["number"]
            if(len(data) == 10):
                data = "+91"+data
            print(data)

            if PhoneNumber.objects.filter(phone_number = data).exists():
                res = PhoneNumber.objects.get(phone_number = data)

                new_dict = {
                    "phone_number":res.phone_number,
                    "carrier":res.carrier,
                    "phone_region":res.phone_region,
                    "is_spam":"true",
                    "spam_marks":res.spam_mark
                }

                return Response(new_dict)
            else:
                print("Start")
                helper_data = get_phone_data(data)
                print("PRINTING HELPER DATA")
                print(helper_data)

                carrier = helper_data["carrier"]
                phone_region = helper_data["phone_region"]

                if(carrier):
                    print("Carrier Found block")
                    new_dict = {
                        "phone_number":data,
                        "carrier":carrier,
                        "phone_region":phone_region,
                        "is_spam":"false",
                        "spam_marks":0
                    }
                    return Response(new_dict)
                elif not carrier:
                    carr = "not_found"
                    print("CArrier not Found block")
                    new_data = {"phone_number":data,"spam_mark":1,"carrier":carr,"phone_region":phone_region}
                    serializer = PhoneNumberSerializer(data=new_data)

                    print("seralizer block start in carrier not found")

                    if serializer.is_valid():
                        print("in seralizer block in carrier not found")
                        serializer.save()
                        print("seralizer block save in carrier not found")
                        new_dict = {
                            "phone_number":data,
                            "carrier":carr,
                            "phone_region":phone_region,
                            "is_spam":"true",
                            "spam_marks":1
                        }

                        return Response(new_dict)
                    else:
                        return Response("Please Enter a Valid Number",status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Please Enter Valid Number",status = status.HTTP_400_BAD_REQUEST)
        
class SpamMark(APIView):
    def put(self,request,**kwargs):
        data = self.kwargs["number"]
        if(len(data) == 10):
            data = "+91"+data
        if PhoneNumber.objects.filter(phone_number=data).exists():
            print("Working start")
            header_data = PhoneNumber.objects.get(phone_number=data)

            spam_marks = header_data.spam_mark+1
            new_dict = {
                "phone_number":header_data.phone_number,
                "carrier":header_data.carrier,
                "phone_region":header_data.phone_region,
                "is_spam":"true",
                "spam_mark":spam_marks
            }
            serializer = PhoneNumberSerializer(header_data,data=new_dict)

            print("WOrking till serilizer")

            if(serializer.is_valid()):
                serializer.save()

                new_dict = {
                        "phone_number":header_data.phone_number,
                        "carrier":header_data.carrier,
                        "phone_region":header_data.phone_region,
                        "is_spam":"true",
                        "spam_marks":header_data.spam_mark
                }

                return Response(new_dict)
            else:
                return Response("Please Provide a valid Phone Number ", status=status.HTTP_400_BAD_REQUEST)
            
        else:
            helper_data = get_phone_data(data)

            carrier = helper_data["carrier"]
            phone_region = helper_data["phone_region"]

            if(not carrier):
                carrier = "not_found"
            new_data = {
                "phone_number" : data,
                "carrier":carrier,
                "phone_region":phone_region,
                "spam_mark":1
            }

            serializer = PhoneNumberSerializer(data=new_data)

            if serializer.is_valid():
                serializer.save()

                new_dict = {
                    "phone_number":data,
                    "carrier":carrier,
                    "phone_region":phone_region,
                    "is_spam":"true",
                    "spam_marks":1
                }

                return Response(new_dict)
            else:
                return Response("Please Provide a valid Phone Number ", status=status.HTTP_400_BAD_REQUEST)


class Test(APIView):
    def get(self,request):
        data = (
            ("GET","/phone/query/<str:number>"),
            ("PUT","/phone/flag_spam/<str:number>"),
        )
        return Response(data)




