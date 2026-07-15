from django.shortcuts import render

# Create your views here.
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    UserSerializer
)
from .renderers import UserJSONRenderer


User = get_user_model()


# ============================================================
#                   HTML АВТОРИЗАЦИЯ (Django View)
# ============================================================

class LoginHTMLView(View):
    """HTML-логин через Django-сессию."""
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next') or 'home_page'
            return redirect(next_url)

        return render(request, 'login.html', {
            'error': 'Неверный логин или пароль'
        })


class RegistrationHTMLView(View):
    """HTML‑регистрация + автоматический вход."""
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'Email уже используется'
            })

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
        )

        login(request, user)
        return redirect('home_page')


class LogoutHTMLView(View):
    """HTML‑логаут (сессия)."""
    def get(self, request):
        logout(request)
        return redirect('home_page')


# ============================================================
#                   JWT API (DRF)
# ============================================================

class RegistrationAPIView(APIView):
    """API‑регистрация с выдачей JWT."""
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data.get('user', {}))
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """API‑логин с выдачей JWT."""
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data.get('user', {}))
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    """API‑профиль текущего пользователя."""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = RegistrationSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = RegistrationSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """API — получить/обновить профиль."""
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    renderer_classes = (UserJSONRenderer,)

    def get_object(self):
        return self.request.user


class LogoutAPIView(APIView):
    """API‑логаут: помещает refresh‑токен в blacklist."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({"error": "Refresh token is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Вы успешно вышли из системы."},
                            status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
