from django.contrib import admin
from .models import Foto, FotosPost, Video, Calendario, Briefing

# Register your models here.

# Registro das Fotos é feito diferente
# "Foto" é principal, "FotosPost" são as fotos em carrossel, uma lista de fotos.
class FotosAdmin(admin.StackedInline):
    model = FotosPost

@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    inlines = [FotosAdmin]

    class Meta:
        model = Foto


@admin.register(FotosPost)
class FotosAdmin(admin.ModelAdmin):
    pass


# Adicionar os models no site do registro
admin.site.register(Video)
admin.site.register(Calendario)
admin.site.register(Briefing)