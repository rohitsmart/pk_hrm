from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login,authenticate
import json
from user.models import User
from user.serializers import UserSerializer,LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def GenerateCredential(request):
 try: 
      if not request.user.ceo_token:
            return Response("Only CEOs can generate credentials", status=403)
      Data= data = request.data.copy()
      username=Data.get('username')
      email=validate_email(Data.get('email'))
      password=username
      if User.objects.filter(email=email).exists():
       return Response("credentials already generated")
      else:
       serializer=UserSerializer(data=Data)
       if serializer.is_valid():
         newUSer=serializer.save(role="employee",password=make_password(password))
         return Response({
            "username":username,
            "password":password
         })
       return Response(serializer.errors, status=400)
    
 except ValidationError as e:
        return Response({
            'user_desc': 'Invalid input provided.',
            'technical_desc': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
 except Exception as e:
        return Response({
            'user_desc': 'Something went wrong.',
            'technical_desc': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
        

@api_view(['POST'])
def login_view(request):
  try:  
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email,password=password)
            if user is None:
                raise ValidationError('Invalid credentials')

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
    else:
              raise ValidationError('Invalid input')
  except ValidationError as e:
        return Response({
            'user_desc': 'Invalid input provided.',
            'technical_desc': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
  except InvalidToken as e:
        return Response({
            'user_desc': 'Invalid token.',
            'technical_desc': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)
  except TokenError as e:
        return Response({
            'user_desc': 'Token error.',
            'technical_desc': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)
  except Exception as e:
        return Response({
            'user_desc': 'Something went wrong.',
            'technical_desc': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)