from django.urls import path
from leaveManagement.views import CreatePolicy,VeiwPolicy,UpdatePolicy,ApplyLeave,ViewLeaves,LeaveList,EditStatus
urlpatterns=[
    path('Create-policy',CreatePolicy),
    path('Veiw-Policy',VeiwPolicy),
    path('UpdatePolicy',UpdatePolicy),
    path('Apply-Leave',ApplyLeave),
    path('View-Leaves',ViewLeaves),
    path('leave-list',LeaveList),
    path('approve-leave',EditStatus)
]