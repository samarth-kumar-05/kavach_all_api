from django.contrib import admin
from django.urls import path

from .views import PhoneQuery,SpamMark,Test,DeletePhoneNumber,HamMark

urlpatterns = [
    path("query/<str:number>", PhoneQuery.as_view(),name="phone_query"),
    path("flag_spam/<str:number>", SpamMark.as_view(),name="Spam_Mark"),
    path("flag_ham/<str:number>", HamMark.as_view(),name="Ham_Mark"),
    path("delete/<str:number>", DeletePhoneNumber.as_view(),name="delete"),
    path("test", Test.as_view(),name="test"),
]
