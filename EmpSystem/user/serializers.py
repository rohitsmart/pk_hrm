# user/serializers.py
from rest_framework import serializers
from user.models import User,profile
from django.contrib.auth.hashers import make_password, check_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'email']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password:
            validated_data['password'] = make_password(password)
        return super().create(validated_data)
    def update(self, instance, validated_data):
        email=validated_data.get('email')
        if User.objects.filter(email=email).exists():
          if validated_data.get('role')!='admin':
            instance.role=validated_data.get('role', instance.role)
            instance.save()
        return instance



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = ['empid', 'userId', 'name', 'contact', 'designation', 'address', 'doj', 'salary', 'qualification', 'email']
     
       

    


