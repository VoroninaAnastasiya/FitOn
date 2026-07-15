from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import UserProfile

User = get_user_model()


class ProfileView(LoginRequiredMixin, View):
    """Просмотр профиля"""
    def get(self, request):
        profile = request.user.profile
        return render(request, 'user_profile/profile.html', {'profile': profile})


class ProfileEditView(LoginRequiredMixin, View):
    """Редактирование профиля"""
    def get(self, request):
        profile = request.user.profile
        return render(request, 'user_profile/profile_edit.html', {'profile': profile})

    def post(self, request):
        profile = request.user.profile

        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.phone_number = request.POST.get('phone_number')
        profile.email = request.POST.get('email')
        profile.date_of_birth = request.POST.get('date_of_birth')

        if request.FILES.get('photo'):
            profile.photo = request.FILES['photo']

        profile.save()
        return redirect('user_profile:profile')


class DeletePhotoView(LoginRequiredMixin, View):
    """Удаление фото профиля"""
    def post(self, request):
        profile = request.user.profile
        if profile.photo:
            profile.photo.delete()
            profile.photo = None
            profile.save()
        return redirect('user_profile:profile')


class DeleteAccountView(LoginRequiredMixin, View):
    """Удаление аккаунта"""
    def post(self, request):
        user = request.user
        logout(request)
        user.delete()
        return redirect('home_page')
