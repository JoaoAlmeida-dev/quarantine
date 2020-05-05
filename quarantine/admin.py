from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Grupo, Publicacao, Comentario, MembroGrupo, VotoComentario, VotoPublicacao

admin.site.register(Grupo)
admin.site.register(MembroGrupo)
admin.site.register(Publicacao)
admin.site.register(Comentario)
admin.site.register(VotoComentario)
admin.site.register(VotoPublicacao)

