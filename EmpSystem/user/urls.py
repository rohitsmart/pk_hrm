from django.urls import path
from .views import GenerateCredential,login_view
urlpatterns=[ path('generateCredential',GenerateCredential),
             path('login',login_view),
            
]