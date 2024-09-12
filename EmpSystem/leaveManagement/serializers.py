from rest_framework import serializers
from leaveManagement.models import leavePolicies,leaveRequest
from datetime import datetime
class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model=leavePolicies
        fields=['leaveType','description','CarryOverLimit','payoutPolicy']

    def update(self, instance, validated_data):
              for field, value in validated_data.items():
                 if field != 'id':  
                    setattr(instance, field, value)
                    instance.save()
              return instance
    
class leaveRequestSerializer(serializers.ModelSerializer):
     class Meta:
          model=leaveRequest
          fields=['id','empId','leaveType','startDate','endDate','duration','status','description','time','approvedBy','approvaldate','approvalTime']  

     status = serializers.CharField(required=False, default='pending')
     approvedBy=serializers.CharField(required=False,default='none')
     time = serializers.TimeField(required=False)
     approvaldate=serializers.DateField(required=False)
     approvalTime=serializers.TimeField(required=False)

     def create(self, validated_data):
        if 'status' not in validated_data:
            validated_data['status'] = 'pending'
        if 'approvedBy' not in validated_data:
            validated_data['approvedBy'] = 'none'    
        if 'time' not in validated_data:
            validated_data['time'] = datetime.now()
        return super().create(validated_data)
     
     def update(self, instance, validated_data):
                instance.status = validated_data.get('status', instance.status)
                now = datetime.now()
                instance.approvaldate = now.date()  
                instance.time = now.time()  
                instance.approvalTime = now.time()
                instance.approvedBy = self.context['request'].user.role
                instance.save()
                return instance
     
     