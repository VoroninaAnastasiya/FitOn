from rest_framework import serializers
from .models import Gym, New, Promotion


class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = '__all__'


class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = New
        fields = '__all__'


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'


class GymDetailSerializer():

    class Meta:
        model = Gym
        fields = '__all__'

    def validate_name(self, value):
        if Gym.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Такой филиал уже существует.")
        return value
