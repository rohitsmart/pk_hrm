from django.shortcuts import render
from datetime import datetime,date
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsAdminUser
from leaveManagement.serializers import PolicySerializer,leaveRequestSerializer
from leaveManagement.models import leavePolicies
from leaveManagement.permissions import IsAdminOrHr,IsAdminOrHrOrManager
from user.models import ProfileCounter
from leaveManagement.models import leaveRequest

@api_view(['POST'])
@permission_classes([ IsAdminUser])
def CreatePolicy(request):
    serializer=PolicySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':"policy created successfully"},status=status.HTTP_200_OK)
    return Response({"message":"some information is missing or invalid"})


@api_view(['GET'])
def VeiwPolicy(request): 
    obj=leavePolicies.objects.all()
    serializer=PolicySerializer(obj,many=True)
    return Response({"data":serializer.data},status=status.HTTP_200_OK)
 
@api_view(['PUT'])
@permission_classes([IsAdminOrHr])
def UpdatePolicy(request):
    try:
        obj=leavePolicies.objects.get(pk=request.data.get('id'))
    except:
        return Response({"message:no such id exist"},status=status.HTTP_404_NOT_FOUND)    
    serialzer=PolicySerializer(obj,data=request.data,partial=True)
    if serialzer.is_valid():
        serialzer.save()
        return Response({"message:policy updated sucessfully"},status=status.HTTP_200_OK)
    print(serialzer.errors)
    return Response({"message:aunthorized access"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def ApplyLeave(request):
    if not ProfileCounter.objects.filter(EmpId=request.data.get('empId')).exists():
      return Response("no such user exist")
    serializer=leaveRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message:successfully applied for leave"},status=status.HTTP_201_CREATED)
    print(serializer.errors) 
    return Response({"message:unable to apply "},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def ViewLeaves(request):
    print('apihit')
    try:
        if not leaveRequest.objects.filter(empId=request.data.get('empId')).exists():
            return Response({"message:no such user exist"})
        
        obj=leaveRequest.objects.filter(empId=request.data.get('empId')).all()
        serializer=leaveRequestSerializer(obj,many=True)
        return Response({"leave detail":serializer.data},status=status.HTTP_200_OK)
    except:
       return Response({"message:no leave is applied"})
    
@api_view(['GET'])
@permission_classes([IsAdminOrHrOrManager])
def LeaveList(request):
   if not leaveRequest.objects.filter(status=request.data.get('status')).exists():
            return Response({"message:no leaves to review"})
   status1=request.data.get('status')
   if status1=='pending':
     obj=leaveRequest.objects.filter(status=status1).all()
   
     serializer=leaveRequestSerializer(obj,many=True)
     return Response({"leave detail":serializer.data},status=status.HTTP_200_OK)
   
@api_view(['PUT'])
@permission_classes([IsAdminOrHrOrManager]) 
def EditStatus(request):
    
    if not leaveRequest.objects.filter(empId=request.data.get('empId')).exists():
            return Response({"either no leave request for this EmpId or invalid EmpId"},status=status.HTTP_400_BAD_REQUEST)
    obj=leaveRequest.objects.get(empId=request.data.get('empId'))
    serializer=leaveRequestSerializer(obj,data=request.data,partial=True, context={'request': request})
    if serializer.is_valid():
      serializer.save()
    return Response({"message:status Updated":serializer.data},status=status.HTTP_200_OK)