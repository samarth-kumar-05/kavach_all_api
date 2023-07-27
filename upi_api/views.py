from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from upi_api.models import UPIAddress
from upi_api.serializers import UPISerializer

from .helper import getNameFromUPI

# Create your views here.

class UpiQuery(APIView):
    def get(self,request,**kwargs):
        try:
            upi_idd = self.kwargs["upi_id"]
            if not UPIAddress.objects.filter(upi_id = upi_idd).exists():
                data = {'upi_id':upi_idd,'spam_mark':0,'ham_mark':0}
                serializer = UPISerializer(data=data)

                if(serializer.is_valid()):
                    serializer.save()
                # updated_data = list(serializer.data)
                name = getNameFromUPI(upi_idd)
                if name==False:
                    return Response("Enter a Valid UPI Address",status=status.HTTP_400_BAD_REQUEST)
                newDict = {'name':name}
                newDict.update(serializer.data)
                print(newDict)
                # updated_data.append({'name':'samarth'})
                return Response(newDict,status=status.HTTP_201_CREATED)
                # return Response(serializer.data, status=status.HTTP_201_CREATED)
            upi_details = UPIAddress.objects.get(upi_id=upi_idd)
        except UPIAddress.DoesNotExist:
           
            return Response("Please Enter a valid UPI address", status=status.HTTP_400_BAD_REQUEST)

        
        serializer = UPISerializer(upi_details)
        # updated_data = list(serializer.data)
        name = getNameFromUPI(upi_idd)
        if name==False:
            return Response("Enter a Valid UPI Address",status=status.HTTP_400_BAD_REQUEST)
        newDict = {'name':name}
        newDict.update(serializer.data)
        print(newDict)
        # updated_data.append({'name':'samarth'})
        return Response(newDict)
    
    # def put(self,request,**kwargs):
    #     upi_idd = self.kwargs["upi_id"]
    #     upi_details = UPIAddress.objects.get(upi_id = upi_idd)

    #     ham_new = upi_details.ham_mark + 1
    #     serializer = UPISerializer(upi_details,data = request.data)

    #     if(serializer.is_valid()):
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class HamMark(APIView):
    def put(self,request,**kwargs):
        upi_idd = self.kwargs["upi_id"]
        upi_details = UPIAddress.objects.get(upi_id = upi_idd)

        ham_new = upi_details.ham_mark + 1
        spam_new = upi_details.spam_mark

        data = {'upi_id':upi_idd,'spam_mark':spam_new,'ham_mark':ham_new}
        serializer = UPISerializer(upi_details,data = data)

        if(serializer.is_valid()):
            serializer.save()
            name = getNameFromUPI(upi_idd)
            if name==False:
                return Response("Enter a Valid UPI Address",status=status.HTTP_400_BAD_REQUEST)
            newDict = {'name':name}
            newDict.update(serializer.data)
            return Response(newDict)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class SpamMark(APIView):
    def put(self,request,**kwargs):
        upi_idd = self.kwargs["upi_id"]
        upi_details = UPIAddress.objects.get(upi_id = upi_idd)

        ham_new = upi_details.ham_mark
        spam_new = upi_details.spam_mark+1

        data = {'upi_id':upi_idd,'spam_mark':spam_new,'ham_mark':ham_new}
        serializer = UPISerializer(upi_details,data = data)

        if(serializer.is_valid()):
            serializer.save()
            name = getNameFromUPI(upi_idd)
            if name==False:
                return Response("Enter a Valid UPI Address",status=status.HTTP_400_BAD_REQUEST)
            newDict = {'name':name}
            newDict.update(serializer.data)
            return Response(newDict)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class Test(APIView):
    def get(self,request):
        data = (
            ("GET","/upi/upi_id"),
            ("PUT","/upi/flag_ham"),
            ("PUT","/upi/flag_spam"),
        )
        return Response(data)
