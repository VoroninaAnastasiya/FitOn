from django.db import models

from gym.models import Gym
from instructor.models import Instructor


class Training(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='trainings', verbose_name='Зал')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Название тренировки')
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='trainings', verbose_name='Инструктор')
    training_time = models.TimeField(verbose_name='Время тренировки')
    start_of_recording = models.TimeField(verbose_name='Начало записи')
    activation = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return f"{self.name} — {self.training_time}"

# class Training(models.Model):
#     gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='trainings', verbose_name='Зал')
#     name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Название тренировки')
#     instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL,
#                                    null=True, blank=True, related_name='trainings', verbose_name='Инструктор')
#
#     date = models.DateField(verbose_name='Дата тренировки')
#     training_time = models.TimeField(verbose_name='Время тренировки')
#     duration = models.PositiveIntegerField(default=60, verbose_name='Длительность (мин)')
#
#     start_of_recording = models.TimeField(verbose_name='Начало записи')
#     activation = models.BooleanField(default=True, verbose_name='Активна')
#
#     def __str__(self):
#         return f"{self.name} — {self.date} {self.training_time}"
