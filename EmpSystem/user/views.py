from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from user.serializers import LoginSerializer,profileSerializer,UserSerializer
from user.models import User,ProfileCounter
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

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProfile(request):
  email=request.data.get('email')
  if not User.objects.filter(email=email): 
    return Response("credentials not generated") 
  else:
    serializer = profileSerializer(data=request.data)
    if serializer.is_valid():
            try:
                latest_id = ProfileCounter.objects.latest('EmpId')
                next_id = latest_id.EmpId + 1
            except ProfileCounter.DoesNotExist:
                next_id = 1000
            serializer.save(empid=next_id)

            new_empId=ProfileCounter(EmpId=next_id)
            new_empId.save()       
    return Response({'message': 'Profile created successfully'}, status=201)
  
@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def UpdateRole(request):
    role=request.data.get('role')
    if not role=='admin':
     email=request.data.get('email')
     user=User.objects.get(email=email)
     serialzer=UserSerializer(user,data=request.data,partial=True)
     if serialzer.is_valid():
        serialzer.save()
        return Response({"message:role updated sucessfully"},status=status.HTTP_204_NO_CONTENT)
    
    return Response({"message:unable to update profile!! invalid email or no credentials exist for this email"},status=status.HTTP_404_NOT_FOUND)
   
