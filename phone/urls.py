from django.contrib import admin
from django.urls import path

from .views import PhoneQuery,SpamMark,Test

urlpatterns = [
    path("/query", PhoneQuery.as_view(),name="phone_query"),
    path("/flag_spam", SpamMark.as_view(),name="Spam_Mark"),
    path("/test", Test.as_view(),name="test"),
]
