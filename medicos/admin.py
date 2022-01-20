from django.contrib import admin
from .models import Foto, Video, Calendario, Briefing

# Register your models here.

admin.site.register(Foto)
admin.site.register(Video)
admin.site.register(Calendario)
admin.site.register(Briefing)