from django.contrib import admin
from django.urls import path

from .views import HeaderQuery,SpamMark,Test

urlpatterns = [
    path("/<str:header>", HeaderQuery.as_view(),name="header_query"),
    path("/flag_spam/<str:header>", SpamMark.as_view(),name="Spam_Mark"),
    path("/", Test.as_view(),name="test"),
]
