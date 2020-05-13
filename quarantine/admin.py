from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Grupo, Publicacao, Comentario, MembroGrupo, VotoComentario, VotoPublicacao


class GrupoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'publico',)
    search_fields = ('titulo', 'publico')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Grupo, GrupoAdmin)

class MembroGrupoAdmin(admin.ModelAdmin):
    list_display = ('id', 'grupo_id', 'account_id', 'is_admin')
    search_fields = ('account_id','grupo_id', 'is_admin')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(MembroGrupo,MembroGrupoAdmin)

class PublicacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'autor_id','grupo_id', 'karma')
    search_fields = ('account_id','grupo_id', 'karma')
    readonly_fields = ('pub_data', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Publicacao,PublicacaoAdmin)

admin.site.register(Comentario)
admin.site.register(VotoComentario)
admin.site.register(VotoPublicacao)

