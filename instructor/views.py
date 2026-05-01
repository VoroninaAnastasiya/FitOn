from django.shortcuts import render
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Instructor
from .serializers import InstructorSerializer


# Create your views here.
class InstructorListCreateView(generics.ListCreateAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer


class InstructorsHTMLView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'instructors_page.html'

    def get(self, request, *args, **kwargs):
        instructors = Instructor.objects.all()
        return Response({'instructors': instructors})


class InstructorDetailHTMLView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'instructor_detail_page.html'

    def get(self, request, pk, *args, **kwargs):
        instructor = Instructor.objects.get(pk=pk)
        trainings = instructor.trainings.all()
        return Response({'instructor': instructor, 'trainings': trainings})
