from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from user.serializers import LoginSerializer
from user.serializers import UserSerializer
from user.permissions import IsAdminUser

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hello(request):
    user = request.user
    return Response({"message": f"Hello, {user.username}! You are authenticated."})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_employee(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(role='employee')
        return Response({
            'message': 'Employee created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
