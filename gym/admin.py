from django.contrib import admin

from .models import Gym, Promotion, New

# Register your models here.
admin.site.register(Gym)
admin.site.register(Promotion)
admin.site.register(New)