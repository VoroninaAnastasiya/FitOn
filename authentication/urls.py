from django.urls import path
from .views import (
    LoginHTMLView,
    RegistrationHTMLView,
    LogoutHTMLView,

    RegistrationAPIView,
    LoginAPIView,
    ProfileAPIView,
    UserRetrieveUpdateAPIView,
    LogoutAPIView
)

urlpatterns = [

    # ============================
    #       HTML AUTH
    # ============================
    path('login/', LoginHTMLView.as_view(), name='login'),
    path('register/', RegistrationHTMLView.as_view(), name='register'),
    path('logout/', LogoutHTMLView.as_view(), name='logout'),

    # ============================
    #       API AUTH (JWT)
    # ============================
    path('api/register/', RegistrationAPIView.as_view(), name='api_register'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/profile/', ProfileAPIView.as_view(), name='api_profile'),
    path('api/user/', UserRetrieveUpdateAPIView.as_view(), name='api_user'),
    path('api/logout/', LogoutAPIView.as_view(), name='api_logout'),
]
