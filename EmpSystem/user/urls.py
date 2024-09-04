from django.urls import path
from .views import GenerateCredential, login_view

urlpatterns = [
    path('generate-credential', GenerateCredential, name='generate-credential'),
    path('login', login_view, name='login'),
]
