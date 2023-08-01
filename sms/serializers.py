from rest_framework import serializers

from sms.models import SMSHeaders

class SMSHeaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = SMSHeaders
        fields = "__all__"
        