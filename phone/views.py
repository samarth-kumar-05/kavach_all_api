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
                    "spam_marks":res.spam_mark,
                    "ham_marks":res.ham_mark,
                }

                return Response(new_dict)
            else:
                print("Start")
                helper_data = get_phone_data(data)
                print("PRINTING HELPER DATA")
                print(helper_data)

                carrier = helper_data["carrier"]
                phone_region = helper_data["phone_region"]

                print(carrier)
                print(phone_region)

                    # print("Carrier Found block")
                    # new_dict = {
                    #     "phone_number":data,
                    #     "carrier":carrier,
                    #     "phone_region":phone_region,
                    #     "is_spam":"false",
                    #     "spam_marks":0
                    # }
                    # return Response(new_dict)
                if not carrier:
                    carrier = "not_found"

                print("Data Ready for serialization")
                
                new_data = {"phone_number":int(data),"spam_mark":0,"carrier":carrier,"phone_region":phone_region,"ham_mark":0}
                serializerr = PhoneNumberSerializer(data=new_data)

                print("seralizer block start in carrier not found")

                if serializerr.is_valid():
                    print("in seralizer block in carrier not found")
                    print(serializerr)
                    serializerr.save()
                    print("seralizer block save in carrier not found")
                    new_dict = {
                        "phone_number":data,
                        "carrier":carrier,
                        "phone_region":phone_region,
                        "spam_marks":0,
                        "ham_mark":0,
                    }


                    print(new_dict)

                    return Response(new_dict)
                else:
                    return Response("Please Enter a Valid Number",status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Please Enter Valid Number except block",status = status.HTTP_400_BAD_REQUEST)
        
    
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
                "spam_mark":spam_marks,
                "ham_mark":header_data.ham_mark
            }
            serializer = PhoneNumberSerializer(header_data,data=new_dict)

            print("WOrking till serilizer")

            if(serializer.is_valid()):
                serializer.save()

                new_dict = {
                        "phone_number":header_data.phone_number,
                        "carrier":header_data.carrier,
                        "phone_region":header_data.phone_region,
                        "spam_marks":header_data.spam_mark,
                        "ham_marks":header_data.ham_mark
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
                "spam_mark":1,
                "ham_mark":0
            }

            serializer = PhoneNumberSerializer(data=new_data)

            if serializer.is_valid():
                serializer.save()

                new_dict = {
                    "phone_number":data,
                    "carrier":carrier,
                    "phone_region":phone_region,
                    "spam_marks":1,
                    "ham_mark":0
                }

                return Response(new_dict)
            else:
                return Response("Please Provide a valid Phone Number ", status=status.HTTP_400_BAD_REQUEST)
        

class HamMark(APIView):
    def put(self,request,**kwargs):
        data = self.kwargs["number"]
        if(len(data) == 10):
            data = "+91"+data
        if PhoneNumber.objects.filter(phone_number=data).exists():
            print("Working start")
            header_data = PhoneNumber.objects.get(phone_number=data)

            ham_mark = header_data.ham_mark+1
            new_dict = {
                "phone_number":header_data.phone_number,
                "carrier":header_data.carrier,
                "phone_region":header_data.phone_region,
                "spam_mark":header_data.spam_mark,
                "ham_mark":ham_mark
            }
            serializer = PhoneNumberSerializer(header_data,data=new_dict)

            print("WOrking till serilizer")

            if(serializer.is_valid()):
                serializer.save()

                new_dict = {
                        "phone_number":header_data.phone_number,
                        "carrier":header_data.carrier,
                        "phone_region":header_data.phone_region,
                        "spam_marks":header_data.spam_mark,
                        "ham_marks":ham_mark
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
                "spam_mark":0,
                "ham_mark":1
            }

            serializer = PhoneNumberSerializer(data=new_data)

            if serializer.is_valid():
                serializer.save()

                new_dict = {
                    "phone_number":data,
                    "carrier":carrier,
                    "phone_region":phone_region,
                    "spam_marks":0,
                    "ham_mark":1
                }

                return Response(new_dict)
            else:
                return Response("Please Provide a valid Phone Number ", status=status.HTTP_400_BAD_REQUEST)
        
class DeletePhoneNumber(APIView):
    def delete(self,request,**kwargs):
            data = self.kwargs["number"]
            print(data)

            if PhoneNumber.objects.filter(phone_number = data).exists():
                res = PhoneNumber.objects.get(phone_number = data)

                res.delete()
                return Response("Phone Number Deleted")
            else:
                return Response("POHONE NUMBER DOES'NT EXIST IN DATABASE")
        


class Test(APIView):
    def get(self,request):
        data = (
            ("GET","/phone/query/<str:number>"),
            ("PUT","/phone/flag_spam/<str:number>"),
        )
        return Response(data)



