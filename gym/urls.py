from django.urls import path
from .views import GymListCreateView, NewsListCreateView, PromotionListCreateView, GymsHTMLView, GymDetailHTMLView, \
    HomeHTMLView

urlpatterns = [
    path('api/gyms/', GymListCreateView.as_view(), name='gym_list'),
    path('api/news/', NewsListCreateView.as_view(), name='news_list'),
    path('api/promotions/', PromotionListCreateView.as_view(), name='promotions_list'),

    path('', HomeHTMLView.as_view(), name='home_page'),
    path('gyms/', GymsHTMLView.as_view(), name='gyms_list'),
    path('gyms/<int:pk>/', GymDetailHTMLView.as_view(), name='gym_detail')
]
