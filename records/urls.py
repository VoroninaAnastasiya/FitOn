from django.urls import path
from .views import WeekTrainingView, CreateRecordView, MyRecordsView

app_name = 'records'

urlpatterns = [
    path('week/', WeekTrainingView.as_view(), name='week_trainings'),
    path('create/<int:training_id>/', CreateRecordView.as_view(), name='create_record'),
    path('my/', MyRecordsView.as_view(), name='my_records'),
]
