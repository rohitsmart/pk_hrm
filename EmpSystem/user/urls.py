from django.urls import path
from .views import login_view,hello,add_employee,createProfile,UpdateRole

urlpatterns = [
    path('login', login_view, name='login'),
    path('hello', hello, name='hello'),
    path('add-employee', add_employee, name='add-employee'),
    path('create-profile',createProfile),
    path('update-role',UpdateRole)
]
