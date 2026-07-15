from django.db import models

class Gym(models.Model):
    address = models.CharField(max_length=255, unique=True, verbose_name='Адрес зала')
    open = models.TimeField(default="08:00", verbose_name="Открытие")
    close = models.TimeField(default="22:00", verbose_name="Закрытие")
    contact_phone = models.CharField(max_length=25, verbose_name='Номер телефона', null=True, blank=True)
    # services = models.ForeignKey(Training, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, verbose_name='Описание зала')
    photo = models.ImageField(
        upload_to='gyms/',
        null=True,
        blank=True,
        verbose_name='Фото зала'
    )

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "Зал (филиал)"
        verbose_name_plural = "Залы (филиалы)"


class New(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='news_list')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class Promotion(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='promotions_list')
    title = models.CharField(max_length=255)
    description = models.TextField()
    valid_until = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
