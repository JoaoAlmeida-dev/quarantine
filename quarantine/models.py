# Create your models here.
from django.contrib.auth.models import User
from django.db import models

from account.models import account




class Grupo(models.Model):
    titulo = models.CharField(max_length=1000, unique=True)
    descrição = models.CharField(max_length=10000)
    membros = models.ManyToManyField(account, through='MembroGrupo')
    publico = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class MembroGrupo(models.Model):
    account = models.ForeignKey(account, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.account + self.grupo


class Publicacao(models.Model):
    titulo = models.CharField(max_length=1000)
    conteudo = models.CharField(max_length=10000)
    pub_data = models.DateTimeField('data de publicacao')

    grupo = models.ForeignKey(Grupo, null=True, on_delete=models.CASCADE)

    autor = models.ForeignKey(account, null=True, on_delete=models.SET_NULL)
    karma = models.IntegerField('votos', default=0)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    publicacao = models.ForeignKey(Publicacao, on_delete=models.CASCADE)
    conteudo = models.CharField(max_length=10000)

    pub_data = models.DateTimeField('data de comentario')

    autor = models.ForeignKey(account, null=True, on_delete=models.SET_NULL)
    karma = models.IntegerField('votos', default=0)
    def __str__(self):
        return self.titulo

class VotoComentario(models.Model):
    autor = models.ForeignKey(account, null=True, on_delete=models.SET_NULL)
    value = models.BooleanField(null=True)
    Comentario = models.ForeignKey(Comentario, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.autor + self.value+ self.Comentario

class VotoPublicacao(models.Model):
    autor = models.ForeignKey(account, null=True, on_delete=models.SET_NULL)
    value = models.BooleanField(null=True)
    Publicacao = models.ForeignKey(Publicacao, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.autor+ self.value +self.Publicacao