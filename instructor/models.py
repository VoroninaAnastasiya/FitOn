from django.db import models

from gym.models import Gym


# Create your models here.
class Instructor(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='instructors', verbose_name='Название зала')
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    experience = models.PositiveIntegerField(verbose_name="Опыт (лет)", default=1)
    photo = models.ImageField(
        upload_to='instructors/',
        null=True,
        blank=True,
        verbose_name='Фото инструктора'
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Инструктор"
        verbose_name_plural = "Инструкторы"
