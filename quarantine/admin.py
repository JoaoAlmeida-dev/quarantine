from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Grupo, Publicacao, Comentario, MembroGrupo, VotoComentario, VotoPublicacao


class GrupoAdmin(admin.ModelAdmin):
    list_display = ('id','titulo', 'publico',)
    search_fields = ('titulo', 'publico')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Grupo, GrupoAdmin)

class MembroGrupoAdmin(admin.ModelAdmin):
    list_display = ('id','grupo', 'account', 'is_admin')
    search_fields = ('account', 'grupo', 'is_admin')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(MembroGrupo,MembroGrupoAdmin)

class PublicacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'grupo','autor', 'karma')
    search_fields = ('autor', 'grupo', 'karma')
    readonly_fields = ('pub_data', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Publicacao,PublicacaoAdmin)

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'publicacao', 'autor', 'karma')
    search_fields = ('autor', 'publicacao', 'karma')
    readonly_fields = ('pub_data', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Comentario,ComentarioAdmin)


class VotoComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'autor', 'value')
    search_fields = ('autor', 'grupo', 'value')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(VotoComentario,VotoComentarioAdmin)

class VotoPublicacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'autor', 'value')
    search_fields = ('autor', 'publicacao', 'value')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(VotoPublicacao,VotoPublicacaoAdmin)

