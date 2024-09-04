# user/views.py
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from user.models import User
from user.serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

@api_view(['POST'])
def login_view(request):
    try:
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
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

# Ensure GenerateCredential is defined or remove this import if not used.
def GenerateCredential(request):
    # Implement the view logic here
    pass
