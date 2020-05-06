from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, Resolver404, resolve
from django.utils import timezone
from django.http import Http404
from django.template import loader
from django.shortcuts import get_object_or_404
from .models import Grupo, Publicacao, Comentario, MembroGrupo, VotoPublicacao, VotoComentario
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
# ------------------------------------------------------------------------


def menu(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('logged', args=()))
    # else:
    grupos = Grupo.objects.filter(membros__id=request.user.id)
    return render(request, 'quarantine/menu.html', {'grupos': grupos})


# ------------------------------------------------------------------------


def loginpage(request):
    return render(request, 'quarantine/login.html')


def loginview(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # existe na BD
        login(request, user)
        return menu(request)
    #    return render(request, 'quarantine/menu.html')
    else:
        # nao existe na BD
        return render(request, 'quarantine/login.html', {'error_message': "Password ou username errados!", })


# ------------------------------------------------------------------------


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return menu(request)


# ------------------------------------------------------------------------


def registopage(request):
    return render(request, 'quarantine/registo.html')


def registview(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']

    user = authenticate(username=username, password=password)
    if user is not None:
        # existe na BD
        return render(request, 'quarantine/registo.html', {'error_message': "User já existe!"})
    else:
        # nao existe na BD
        User.objects.create_user(username, email, password)
        return menu(request)


# ----------------------------------------------------------------------


def criargrupopage(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'quarantine/criargrupopage.html', {'users': users})


def criargrupo(request):
    g = Grupo(titulo=request.POST['titulo'], descrição=request.POST['desc'])
    g.save()

    mg = MembroGrupo(user=request.user, grupo=g, is_admin=True)
    mg.save()
    for username in request.POST.getlist('user'):
        mg = MembroGrupo(user=User.objects.get(username=username), grupo=g, is_admin=False)
        mg.save()
    g.save()
    return HttpResponseRedirect(reverse('menu', args=()))


def apagargrupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)

    # for membrogrupo in MembroGrupo.objects.filter(grupo_id=grupo_id, user_id=request.user.id):
    # if membrogrupo.is_admin:

    if MembroGrupo.objects.get(grupo_id=grupo_id, user_id=request.user.id).is_admin:
        grupo.delete()
        return HttpResponseRedirect(reverse('menu', args=()))
    else:
        return render(request, 'quarantine/grupo.html', {'grupo': grupo, 'error_message': "Não é admin do grupo!!"})
    # if grupo.membrogrupo_set.get(id=request.user.id, user_id=request.user.id).is_admin:


# ----------------------------------------------------------------------


def grupo_view(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    isadmin = MembroGrupo.objects.get(grupo_id=grupo_id, user_id=request.user.id).is_admin
    return render(request, 'quarantine/grupo.html', {'grupo': grupo, 'isadmin': isadmin})


def criarpublicacaopage(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    return render(request, 'quarantine/criarpublicacaopage.html', {'grupo': grupo})


def criarpublicacao(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    pub = Publicacao(pub_data=timezone.now(), titulo=request.POST['titulo'], conteudo=request.POST['conteudo'],
                     autor=request.user, grupo=grupo)
    pub.save()
    candeletepub = MembroGrupo.objects.get(grupo_id=grupo_id,
                                           user_id=request.user.id).is_admin or pub.autor.id == request.user.id
    return render(request, 'quarantine/publicacao.html', {'grupo': grupo, 'pub': pub, 'candeletepub': candeletepub})


def apagarpublicacao(request, grupo_id, pub_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    pub = get_object_or_404(Publicacao, pk=pub_id)

    candeletepub = MembroGrupo.objects.get(grupo_id=grupo_id,
                                           user_id=request.user.id).is_admin or pub.autor.id == request.user.id
    isadmin = MembroGrupo.objects.get(grupo_id=grupo_id, user_id=request.user.id).is_admin

    if candeletepub:
        pub.delete()
        return grupo_view(request, grupo_id)
        #return HttpResponseRedirect(reverse('grupo_view', args=grupo_id))
        #return render(request, 'quarantine/grupo.html', {'grupo': grupo, 'isadmin': isadmin})
    else:
        return render(request, 'quarantine/publicacao.html', {'grupo': grupo,
                                                              'pub': pub,
                                                              'error_message':
                                                                  "Não é admin do grupo ou autor da publicação!!"})


def adicionarmembrospage(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    membros = MembroGrupo.objects.filter(grupo_id=grupo_id)
    users = User.objects.exclude(id=request.user.id)
    for membro in membros:
        users = users.exclude(id=membro.user_id)

#    url = request.GET.get("next")
    return render(request, 'quarantine/adicionarmembrospage.html', {'grupo': grupo, 'users': users,
                                                                    #'next': url
                                                                    })


def adicionarmembros(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)

#    url = request.GET.get("next")
#    try:
#        resolve(url)
    for username in request.POST.getlist('user'):
        mg = MembroGrupo(user=User.objects.get(username=username), grupo=grupo, is_admin=False)
        mg.save()
    #return HttpResponseRedirect(reverse('grupo_view', args=grupo_id))
    return grupo_view(request, grupo_id)
#        return HttpResponseRedirect(url)

#    except (KeyError, Resolver404):
#        return HttpResponseRedirect(reverse('menu'))

# ----------------------------------------------------------------------


def publicacao(request, grupo_id, pub_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    pub = get_object_or_404(Publicacao, pk=pub_id)
    isadmin = MembroGrupo.objects.get(grupo_id=grupo_id, user_id=request.user.id).is_admin

    return render(request, 'quarantine/publicacao.html', {'grupo': grupo, 'pub': pub, 'isadmin': isadmin})


def publicarcomentario(request, grupo_id, pub_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    pub = get_object_or_404(Publicacao, pk=pub_id)
    url = request.GET.get("next")
    try:
        resolve(url)

        com = Comentario(conteudo=request.POST['conteudo'], pub_data=timezone.now(), karma=0, autor=request.user,
                         publicacao=pub)
        com.save()
        #return HttpResponseRedirect(reverse('publicacao', args=(grupo_id, pub_id)))
        return HttpResponseRedirect(url)
    except (KeyError, Resolver404):
        return HttpResponseRedirect(reverse('menu'))

def apagarcomentario(request, grupo_id, pub_id, com_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    pub = get_object_or_404(Publicacao, pk=pub_id)
    com = get_object_or_404(Comentario, pk=com_id)

    candeletepub = MembroGrupo.objects.get(grupo_id=grupo_id, user_id=request.user.id).is_admin or \
                   pub.autor.id == request.user.id
    candeletecom = MembroGrupo.objects.get(grupo_id=grupo_id, user_id=request.user.id).is_admin or \
                   com.autor.id == request.user.id

    if candeletecom:
        com.delete()
        return publicacao(request, grupo_id, pub_id)
        # return render(request, 'quarantine/publicacao.html', {'grupo': grupo, 'pub': pub, 'candeletepub': candeletepub, 'candeletecom': candeletecom})
        # return HttpResponseRedirect(reverse('publicacao', args=(grupo_id, pub_id)))
    else:
        return render(request, 'quarantine/publicacao.html', {'grupo': grupo,
                                                              'pub': pub, 'error_message': "Não é admin do grupo ou "
                                                                                           "autor do comentario!!"})

# ----------------------------------------------------------------------

def votarupcom(request, grupo_id, pub_id, com_id):
    com = get_object_or_404(Comentario, pk=com_id)

    url = request.GET.get("next")
    try:
        resolve(url)
        try:
            voto = get_object_or_404(VotoComentario, autor=request.user, Comentario=com)
        except(KeyError, Http404):
            voto = VotoComentario(autor=request.user, value=True, Comentario=com)
            com.karma += 1
            com.save()
            voto.save()
            return HttpResponseRedirect(url)
        else:
            if voto.value:
                com.karma -= 1
                voto.delete()
            else:
                com.karma += 2
                voto.value = True
                voto.save()
        com.save()
        return HttpResponseRedirect(url)
    except (KeyError, Resolver404):
        return HttpResponseRedirect(reverse('menu'))

def votardowncom(request, grupo_id, pub_id, com_id):
    com = get_object_or_404(Comentario, pk=com_id)
    url = request.GET.get("next")
    try:
        resolve(url)
        try:
            voto = get_object_or_404(VotoComentario, autor=request.user, Comentario=com)
        except(KeyError, Http404):
            voto = VotoComentario(autor=request.user, value=False, Comentario=com)
            com.karma -= 1
            com.save()
            voto.save()
            return HttpResponseRedirect(url)
        else:
            if voto.value:
                com.karma -= 2
                voto.value = False
                voto.save()
            else:
                com.karma += 1
                voto.delete()

        com.save()
        return HttpResponseRedirect(url)
    except (KeyError, Resolver404):
        return HttpResponseRedirect(reverse('menu'))

# ----------------------------------------------------------------------


def votaruppub(request, grupo_id, pub_id):
    url = request.GET.get("next")
    pub = get_object_or_404(Publicacao, pk=pub_id)

    url = request.GET.get("next")
    try:
        resolve(url)
        try:
            voto = get_object_or_404(VotoPublicacao, autor=request.user, Publicacao=pub)
        except(KeyError, Http404):
            voto = VotoPublicacao(autor=request.user, value=True, Publicacao=pub)
            pub.karma += 1
            pub.save()
            voto.save()
            return HttpResponseRedirect(url)
        else:
            if voto.value:
                pub.karma -= 1
                voto.delete()
            else:
                pub.karma += 2
                voto.value = True
                voto.save()
        pub.save()
        return HttpResponseRedirect(url)
    except (KeyError, Resolver404):
        return HttpResponseRedirect(reverse('menu'))


def votardownpub(request, grupo_id, pub_id):
    pub = get_object_or_404(Publicacao, pk=pub_id)
    url = request.GET.get("next")
    try:
        resolve(url)
        try:
            voto = get_object_or_404(VotoPublicacao, autor=request.user, Publicacao=pub)
        except(KeyError, Http404):
            voto = VotoPublicacao(autor=request.user, value=False, Publicacao=pub)
            pub.karma -= 1
            pub.save()
            voto.save()
            return HttpResponseRedirect(url)
        else:
            if voto.value:
                pub.karma -= 2
                voto.value = False
                voto.save()
            else:
                pub.karma += 1
                voto.delete()

        pub.save()
        return HttpResponseRedirect(url)
    except (KeyError, Resolver404):
        return HttpResponseRedirect(reverse('menu'))

# ----------------------------------------------------------------------

