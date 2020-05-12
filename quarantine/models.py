# Create your models here.
from django.contrib.auth.models import User
from django.db import models

from account.models import Account




class Grupo(models.Model):
    titulo = models.CharField(max_length=1000)
    descrição = models.CharField(max_length=10000)
    membros = models.ManyToManyField(Account, through='MembroGrupo')

    def __str__(self):
        return self.titulo


class MembroGrupo(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)


class Publicacao(models.Model):
    titulo = models.CharField(max_length=1000)
    conteudo = models.CharField(max_length=10000)
    pub_data = models.DateTimeField('data de publicacao')

    grupo = models.ForeignKey(Grupo, null=True, on_delete=models.CASCADE)

    autor = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    karma = models.IntegerField('votos', default=0)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    publicacao = models.ForeignKey(Publicacao, on_delete=models.CASCADE)
    conteudo = models.CharField(max_length=10000)

    pub_data = models.DateTimeField('data de comentario')

    autor = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    karma = models.IntegerField('votos', default=0)


class VotoComentario(models.Model):
    autor = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    value = models.BooleanField(null=True)
    Comentario = models.ForeignKey(Comentario, null=True, on_delete=models.SET_NULL)


class VotoPublicacao(models.Model):
    autor = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    value = models.BooleanField(null=True)
    Publicacao = models.ForeignKey(Publicacao, null=True, on_delete=models.SET_NULL)
