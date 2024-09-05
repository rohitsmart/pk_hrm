from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from user.serializers import LoginSerializer,GenerateCredentialSerializer
from user.models  import User
from django.contrib.auth.hashers import make_password
from user.permissions import IsAdmin



@api_view(['POST'])
def login_view(request):
    try:
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            print("email",email)
            print("password",password)
            user = authenticate(request, email=email, password=password)
            print("user",user)

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
@permission_classes([IsAuthenticated,IsAdmin])
def GenerateCredential(request):
    email=request.data.get("email")
    print(email)
    if User.objects.filter(email=email):
        return Response("credentials already generated",status=status.HTTP_400_BAD_REQUEST)
    
    str=''
    for i in email:
        if i=='@':
            break
        str+=i
    password= 'password'
    username=str
    serializer=GenerateCredentialSerializer(data={
        "email":email,
        "username":username,
        "password":make_password(password),
        "role":"employee"
    })
    serializer.is_valid()
    serializer.save()
    return Response({
        "message":"credential generated successfully",
         "email":email,
        "username":username,
        "password":password
    })