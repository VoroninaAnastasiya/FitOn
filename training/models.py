from datetime import datetime
from django.db import models
from gym.models import Gym
from instructor.models import Instructor
from django.utils import timezone


# class Training(models.Model):
#     gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='trainings', verbose_name='Зал')
#     name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Название тренировки')
#     instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL,
#                                    null=True, blank=True, related_name='trainings', verbose_name='Инструктор')
#     training_time = models.TimeField(verbose_name='Время тренировки')
#     start_of_recording = models.TimeField(verbose_name='Начало записи')
#     activation = models.BooleanField(default=True, verbose_name='Активна')
#
#     def __str__(self):
#         return f"{self.name} — {self.training_time}"

class Training(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='trainings', verbose_name='Зал')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Название тренировки')
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='trainings', verbose_name='Инструктор')

    date = models.DateField(verbose_name='Дата тренировки')
    training_time = models.TimeField(verbose_name='Время тренировки')
    duration = models.PositiveIntegerField(default=60, verbose_name='Длительность (мин)')
    max_participants = models.PositiveIntegerField(default=10, verbose_name='Количество мест')
    start_of_recording = models.TimeField(verbose_name='Начало записи') # todo datetime field
    activation = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return f"{self.name} — {self.date} {self.training_time}"

    class Meta:
        verbose_name = "Тренировка"
        verbose_name_plural = "Тренировки"


    @property
    def start_datetime(self):
        """Полная дата и время начала тренировки."""
        return timezone.make_aware(
            datetime.combine(
                self.date,
                self.training_time
            )
        )

    @property
    def is_finished(self):
        """Тренировка уже прошла."""
        return self.start_datetime < timezone.now()

    @property
    def free_places(self):
        """Количество свободных мест."""
        return self.max_participants - self.records.count()

    @property
    def is_available_for_booking(self):
        """Доступна ли запись."""
        return (
                not self.is_finished
                and self.free_places > 0
                and self.activation
        )
