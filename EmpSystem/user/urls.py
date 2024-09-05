from django.urls import path
from .views import login_view,hello

urlpatterns = [
    path('login', login_view, name='login'),
    path('hello', hello, name='hello'),

]
