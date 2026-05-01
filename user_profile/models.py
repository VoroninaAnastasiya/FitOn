from django.db import models

from gym.models import Gym


class UserProfile(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=25)
    email = models.EmailField()
    fit_address = models.ForeignKey(
        Gym,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='profiles',
        verbose_name="Посещаемый зал"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name
