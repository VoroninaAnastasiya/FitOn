from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from training.models import Training


# Create your views here.
class TrainingHTMLView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'trainings.html'


    def get(self, request, *args, **kwargs):
        trainings = Training.objects.all()
        return Response({'trainings': trainings})