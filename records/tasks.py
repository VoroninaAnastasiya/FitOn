from celery import shared_task
from training.models import Training
from datetime import datetime
import os
from django.conf import settings


@shared_task
def check_trainings():
    # считаем активные тренировки
    count = Training.objects.filter(activation=True).count()

    # пишем в лог-файл
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_path = os.path.join(settings.BASE_DIR, "celery_check.txt")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{now}] Активных тренировок: {count}\n")

    return f"Активных тренировок: {count}"
