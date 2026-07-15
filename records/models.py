from django.db import models
from user_profile.models import UserProfile
from training.models import Training

# class TrainingRecord(models.Model):
#     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
#                              related_name='records', verbose_name='Пользователь')
#     training = models.ForeignKey(Training, on_delete=models.CASCADE,
#                                  related_name='records', verbose_name='Тренировка')
#     date = models.DateField(verbose_name='Дата тренировки')
#     created_at = models.DateField(auto_now_add=True)
#
#     class Meta:
#         verbose_name = "Запись на тренировку"
#         verbose_name_plural = "Записи на тренировки"
#         unique_together = ('user', 'training', 'date')
#
#     def __str__(self):
#         return f"{self.user.full_name} → {self.training.name} ({self.date})"


class TrainingRecord(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='records',
        verbose_name='Пользователь'
    )
    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        related_name='records',
        verbose_name='Тренировка'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Запись на тренировку"
        verbose_name_plural = "Записи на тренировки"
        unique_together = ('user', 'training')

    def __str__(self):
        return f"{self.user.full_name} → {self.training.name} ({self.training.date})"


