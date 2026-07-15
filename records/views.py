from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.context_processors import request
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from user_profile.models import UserProfile
from training.models import Training
from records.models import TrainingRecord

# Create your views here.
class WeekTrainingView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'week_trainings.html'

    def get(self, request):
        trainings = Training.objects.filter(activation = True
                                       ).select_related('instructor', 'gym').order_by('training_time')
        print("TRAININGS:", Training.objects.filter(activation=True))
        return Response({'trainings': trainings})


class CreateRecordView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request, training_id):
        training = get_object_or_404(Training, id=training_id)
        return render(request, 'records/create_record.html', {
            'training': training,
            'profile': request.user.profile  # теперь работает
        })

    def post(self, request, training_id):
        training = get_object_or_404(Training, id=training_id)

        # создаём запись
        record, created = TrainingRecord.objects.get_or_create(
            user=request.user.profile,   # теперь корректно
            training=training
        )

        if created:
            messages.success(request, 'Вы успешно записались на тренировку')
        else:
            messages.info(request, 'Вы уже записаны на эту тренировку')

        return redirect('records:my_records')
# class CreateRecordView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'create_record.html'
#
#     def get(self, request, training_id):
#         training = get_object_or_404(Training, id=training_id)
#         return Response({'training': training})
#
#     def post(self, request, training_id):
#         training = get_object_or_404(Training, id=training_id)
#         user_profile = get_object_or_404(UserProfile, email=request.user.email)
#
#         # Проверяем, есть ли уже запись
#         record, created = TrainingRecord.objects.get_or_create(
#             user=user_profile,
#             training=training
#         )
#
#         if created:
#             messages.success(request, 'Вы успешно записались на тренировку')
#         else:
#             messages.info(request, 'Вы уже записаны на эту тренировку')
#
#         return redirect('records:my_records')



class MyRecordsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'my_records.html'

    def get(self,request):
        user_profile = get_object_or_404(UserProfile, email=request.user.email)

        records = TrainingRecord.objects.filter(user=user_profile).select_related('training', 'training__instructor',
                                                                                  'training__gym').order_by('training__date')

        return Response({'records': records})

# class CreateRecordView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'create_record.html'
#
#     def get(self, request, training_id):
#         training = get_object_or_404(Training, id=training_id)
#         return Response({'training': training})
#
#     def post(self, request, training_id):
#         training = get_object_or_404(Training, id=training_id)
#         user_profile = get_object_or_404(UserProfile, email=request.user.email)
#
#         record, created = TrainingRecord.objects.get_or_create(
#             user=user_profile,
#             training=training
#         )
#
#         if created:
#             messages.success(request, 'Вы успешно записались')
#         else:
#             messages.info(request, 'Вы уже записаны на эту тренировку')
#
#         return redirect('records:my_records')