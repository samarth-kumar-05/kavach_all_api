from rest_framework import serializers


from upi_api.models import UPIAddress

class UPISerializer(serializers.ModelSerializer):
    class Meta:
        model = UPIAddress
        fields = "__all__"

class UPICustomSerializer(serializers.Serializer):
    upi_id = serializers.CharField()
    # name = serializers.CharField(validators=[name_length])
    spam_mark = serializers.IntegerField()
    ham_mark = serializers.IntegerField()

    def create(self,validated_data):
        return UPIAddress.objects.create(**validated_data)
    
    # def update(self,instace,validated_data):
    #     # instace is the current data and validated data is the new value that has been updated
    #     instace.name = validated_data.get('name',instace.name)
    #     instace.description = validated_data.get('description',instace.description)
    #     instace.active = validated_data.get('active',instace.active)
    #     instace.save()
    #     return instace
    
    #validator
    def validate(self, data):
        print(" ")
        print(" ")
        print(" ")
        print(data)
        print(" ")
        print(" ")
        print(" ")
        if not data['upi_id']:
            raise serializers.ValidationError('Please enter a upi address')
        return data

    # def validate_name(self,value):
    #     if len(value) > 30:
    #         raise serializers.ValidationError('Name must be less than 30 characters')
    #     else:
    #         return value
