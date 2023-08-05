from django.contrib import admin
from django.urls import path

from .views import UpiQuery,Test,HamMark,SpamMark

urlpatterns = [
    path("<str:upi_id>", UpiQuery.as_view(),name="upi_query"),
    path("flag_ham/<str:upi_id>", HamMark.as_view(),name="Ham Mark"),
    path("flag_spam/<str:upi_id>", SpamMark.as_view(),name="Spam Mark"),
    path("", Test.as_view(),name="test"),
]
