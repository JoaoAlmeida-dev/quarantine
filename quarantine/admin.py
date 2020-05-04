from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Grupo, Publicacao, Comentario, MembroGrupo

admin.site.register(Grupo)
admin.site.register(MembroGrupo)
admin.site.register(Publicacao)
admin.site.register(Comentario)

