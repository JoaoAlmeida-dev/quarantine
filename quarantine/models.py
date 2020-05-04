# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Grupo(models.Model):
    titulo = models.CharField(max_length=1000)
    descrição = models.CharField(max_length=10000)
    membros = models.ManyToManyField(User, through='MembroGrupo')

    def __str__(self):
        return self.titulo


class MembroGrupo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)


class Publicacao(models.Model):
    pub_data = models.DateTimeField('data de publicacao')
    titulo = models.CharField(max_length=1000)
    conteudo = models.CharField(max_length=10000)
    autor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    grupo = models.ForeignKey(Grupo, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    conteudo = models.CharField(max_length=10000)
    karma = models.IntegerField('votos', default=0)
    pub_data = models.DateTimeField('data de comentario')
    autor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    publicacao = models.ForeignKey(Publicacao, on_delete=models.CASCADE)

    def __str__(self):
        return self.conteudo
