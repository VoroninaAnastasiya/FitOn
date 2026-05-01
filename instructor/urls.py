from django.urls import path
from .views import (
    InstructorsHTMLView,
    InstructorDetailHTMLView,
    InstructorListCreateView,

)

urlpatterns = [
    # HTML
    path('instructors/', InstructorsHTMLView.as_view(), name='instructors_list'),
    path('instructors/<int:pk>/', InstructorDetailHTMLView.as_view(), name='instructor_detail'),

    # API
    path('api/instructors/', InstructorListCreateView.as_view(), name='instructors_api'),
]
