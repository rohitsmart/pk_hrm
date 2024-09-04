from rest_framework import serializers
from user.models import User
from django.contrib.auth.hashers import make_password
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','password','role','email']
    def create(self, validated_data):
        validated_data['password'] = (validated_data['password'])
        return super().create(validated_data)    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    