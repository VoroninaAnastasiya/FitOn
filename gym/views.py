from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from training.models import Training
from instructor.models import Instructor
from .models import Gym, New, Promotion
from .serializers import GymSerializer, NewSerializer, PromotionSerializer, GymDetailSerializer

class HomeHTMLView(APIView):
    """
    HTML‑представление главной страницы сайта.

    Назначение:
    - служит точкой входа для пользователя;
    - отображает краткую информацию о сети залов и тренерах;
    - предоставляет навигацию к списку залов и тренеров;
    - рендерит шаблон home_page.html.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home_page.html'

    def get(self, request, *args, **kwargs):
        """
        Возвращает контекст для главной страницы:
        - список залов (для блока «Наши залы»);
        - список тренеров (для блока «Наши тренеры»);
        - базовые данные для навигации.
        """
        gyms = Gym.objects.all()[:3]  # показываем первые 3 зала
        instructors = Instructor.objects.all()[:4]  # показываем первых 4 тренера

        context = {
            'gyms': gyms,
            'instructors': instructors,
            'page_title': 'Главная — Сеть тренажёрных залов Минска',
        }
        return Response(context)

class GymsHTMLView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'gyms.html'


    def get(self, request, *args, **kwargs):
        gyms = Gym.objects.all()
        return Response({'gyms': gyms})


class GymDetailHTMLView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'gym_detail.html'

    def get(self, request, pk, *args, **kwargs):
        gym = Gym.objects.get(pk=pk)
        trainings = gym.trainings.all()
        instructors = gym.instructors.all()

        return Response({
            'gym': gym,
            'trainings': trainings,
            'instructors': instructors,
        })


class GymListCreateView(generics.ListCreateAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer


class NewsListCreateView(generics.ListCreateAPIView):
    queryset = New.objects.all()
    serializer_class = NewSerializer


class PromotionListCreateView(generics.ListCreateAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


