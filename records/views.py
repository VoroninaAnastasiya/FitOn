from django.template.context_processors import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import get_object_or_404, redirect
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
        return Response({'trainings': trainings})


class CreateRecordView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'create_record.html'

    def get(self,request, training_id):
        training = get_object_or_404(Training, id=training_id)
        return Response({'training': training})

    def post(self,request, training_id):
        training = get_object_or_404(Training, id=training_id)
        user_profile  = get_object_or_404(UserProfile, email=request.user.email)
        data = request.POST.get('data')
        if not data:
            messages.error(request, 'выберете дату')
            return redirect('records:create_record', training_id=training.id)

        record, created = TrainingRecord.objects.get_or_create(
            user=user_profile,
            training=training,
            date=data
        )
        if created:
            messages.success(request, 'Вы успешно записаны на тренировку')
        else:
            messages.info(request, 'Вы уже записаны на эту тренировку')

        return redirect('records:my_records')


class MyRecordsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'my_records.html'

    def get(self,request):
        user_profile = get_object_or_404(UserProfile, email=request.user.email)

        records = TrainingRecord.objects.filter(user=user_profile).select_related('training', 'training__instructor',
                                                                                  'training__gym').order_by('date')

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