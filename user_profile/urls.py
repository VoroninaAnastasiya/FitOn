from django.urls import path
from .views import (
    ProfileView,
    ProfileEditView,
    DeletePhotoView,
    DeleteAccountView
)

app_name = 'user_profile'

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('delete-photo/', DeletePhotoView.as_view(), name='delete_photo'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
]
