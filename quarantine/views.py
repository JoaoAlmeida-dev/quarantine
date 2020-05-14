from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, Resolver404, resolve
from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Grupo, Publicacao, Comentario, MembroGrupo, VotoPublicacao, VotoComentario
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.db.models import Q, Exists

from django.core.exceptions import ObjectDoesNotExist
from account.models import Account


# Create your views here.
# ------------------------------------------------------------------------

def is_admin(request, grupo_id):
    if request.user.is_admin or is_membro(request, grupo_id):
        if request.user.is_admin or MembroGrupo.objects.get(grupo_id=grupo_id, account=request.user).is_admin:
            return True
        else:
            return False
    else:
        return False


def is_membro(request, grupo_id):
    try:
        MembroGrupo.objects.get(grupo_id=grupo_id, account=request.user)
    except (KeyError, ObjectDoesNotExist):
        return False
    else:
        return True


def menu(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('logged', args=()))
    # else:
    grupos = Grupo.objects.filter(Q(membros__id=request.user.id) | Q(publico=True)).distinct().order_by('titulo')

    return render(request, 'quarantine/menu.html', {'grupos': grupos, 'titulo': 'Os seus grupos e Grupos Públicos'})


# ----------------------------------------------------------------------

def sobre(request):
    return render(request, 'quarantine/sobre.html')


def contactos(request):
    return render(request, 'quarantine/contactos.html')


# ----------------------------------------------------------------------

def grupospublicos(request):
    grupos = Grupo.objects.filter(publico=True).order_by('titulo')
    return render(request, 'quarantine/menu.html', {'grupos': grupos, 'titulo': 'Grupos Públicos'})


def gruposutilizador(request):
    grupos = Grupo.objects.filter(membros__id=request.user.id).order_by('titulo')
    return render(request, 'quarantine/menu.html', {'grupos': grupos, 'titulo': 'Os seus grupos'})


def gruposprivados(request):
    if request.user.is_admin:
        grupos = Grupo.objects.filter(publico=False).order_by('titulo')
    else:
        grupos = Grupo.objects.filter(publico=False, membros__id=request.user.id).order_by('titulo')
    return render(request, 'quarantine/menu.html', {'grupos': grupos, 'titulo': 'Grupos Privados'})


# ------------------------------------------------------------------------

# def atualizarperfil(request, username):
#     user = get_object_or_404(Account, username=username)
#     if user.id == request.user.id:
#         user.set_password(request.POST['password'])
#         user.email = request.POST['email']
#         user.username = request.POST['username']
#         user.save()
#         return logout(request)
#     else:
#         return render(request, 'quarantine/perfil.html',
#                       {'username': user.usernamem, 'error_message': "Nao pode alterar as definições de outro user"})


# ----------------------------------------------------------------------


# def criargrupopage(request):
#    users = User.objects.exclude(username=request.user.username)
#    return render(request, 'quarantine/criargrupo.html', {'users': users})


def criargrupo(request):
    if request.POST:
        visibilidade = request.POST['visibilidade']
        if visibilidade == 'publico':
            g = Grupo(titulo=request.POST['titulo'], descrição=request.POST['desc'], publico=True)
        if visibilidade == 'privado':
            g = Grupo(titulo=request.POST['titulo'], descrição=request.POST['desc'], publico=False)

        g.save()

        mg = MembroGrupo(account=request.user, grupo=g, is_admin=True)
        mg.save()
        for username in request.POST.getlist('user'):
            mg = MembroGrupo(
                account=Account.objects.get(username=username), grupo=g, is_admin=False)
            mg.save()
        g.save()
        return HttpResponseRedirect(reverse('menu', args=()))
    else:
        users = Account.objects.exclude(username=request.user.username)
        return render(request, 'quarantine/criargrupo.html', {'users': users})


def apagargrupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)

    # for membrogrupo in MembroGrupo.objects.filter(grupo_id=grupo_id, Account_id=request.user.id):
    # if membrogrupo.is_admin:

    if is_admin(request, grupo_id):
        grupo.delete()
        return HttpResponseRedirect(reverse('menu', args=()))
    else:
        HttpResponseRedirect(reverse('menu', kwargs={'grupo': grupo, 'error_message': "Não é admin do grupo!!"}))
        # return render(request, 'quarantine/grupo.html', )
    # if grupo.membrogrupo_set.get(id=request.user.id, Account_id=request.user.id).is_admin:


# ----------------------------------------------------------------------


def grupo_view(request, grupo_id):
    membro = None
    admin = is_admin(request, grupo_id)

    try:
        grupo = get_object_or_404(Grupo, pk=grupo_id)
    except (KeyError, ObjectDoesNotExist):
        # Não existe grupo com esse id
        return HttpResponseRedirect(reverse('menu'))
    else:
        publicacoes = Publicacao.objects.filter(grupo_id=grupo_id).order_by('-karma', 'titulo')

        ismembro = is_membro(request, grupo_id)

        if grupo.publico:
            membrosgrupo = MembroGrupo.objects.filter(grupo_id=grupo_id).order_by('MembroGrupo_account__username')
            return render(request, 'quarantine/grupo.html',
                          {'grupo': grupo, 'membrosgrupo': membrosgrupo, 'publicacoes': publicacoes,
                           'ismembro': ismembro, 'isadmin': admin})
        else:
            membrosgrupo = MembroGrupo.objects.filter(grupo_id=grupo_id).order_by('MembroGrupo_account__username')
            if not admin:
                membro = membrosgrupo.get(grupo_id=grupo_id, account=request.user)
            return render(request, 'quarantine/grupo.html',
                          {'grupo': grupo, 'membrosgrupo': membrosgrupo, 'publicacoes': publicacoes,
                           'ismembro': ismembro, 'isadmin': admin})


def criarpublicacao(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    context = {}
    context['grupo'] = grupo
    if request.POST:
        ismembro = is_membro(request, grupo_id)

        if not ismembro:
            return HttpResponseRedirect(reverse('grupo_view', kwargs={'grupo_id': grupo_id, 'ismembro': False,
                                                                      'error_message': 'Nao pode publicar num grupo onde nao pertence'}))

        pub = Publicacao(pub_data=timezone.now(), titulo=request.POST['titulo'], conteudo=request.POST['conteudo'],
                         autor=request.user, grupo=grupo)

        pub.save()
        candeletepub = MembroGrupo.objects.get(grupo_id=grupo_id, account_id=request.user.id).is_admin \
                       or pub.autor.id == request.user.id
        context['pub'] = pub
        context['candeletepub'] = candeletepub
        # return render(request, 'quarantine/publicacao.html', context)
        return redirect('publicacao', grupo_id=grupo.id, pub_id=pub.id)
    else:
        return render(request, 'quarantine/criarpublicacaopage.html', {'grupo': grupo})


def apagarpublicacao(request, grupo_id, pub_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    pub = get_object_or_404(Publicacao, pk=pub_id)

    candeletepub = is_admin(request, grupo_id) or pub.autor.id == request.user.id
    # isadmin = MembroGrupo.objects.get(grupo_id=grupo_id, Account_id=request.user.id).is_admin

    if candeletepub:
        pub.delete()
        ismembro = is_membro(request, grupo_id)

        return HttpResponseRedirect(reverse('grupo_view', kwargs={'grupo_id': grupo_id}))

        # return render(request, 'quarantine/grupo.html', {'grupo': grupo, 'isadmin': isadmin})
    else:
        return render(request, 'quarantine/publicacao.html', {'grupo': grupo, 'pub': pub, 'error_message':
            "Não é admin do grupo ou autor da publicação!!"})


# def adicionarmembrospage(request, grupo_id):
# grupo = get_object_or_404(Grupo, pk=grupo_id)
# membros = MembroGrupo.objects.filter(grupo_id=grupo_id)
# users = User.objects.exclude(id=request.user.id)
#   for membro in membros:


#   users = users.exclude(id=membro.Account_id)

#    url = request.GET.get("next")
#    return render(request, 'quarantine/adicionarmembros.html', {'grupo': grupo, 'users': users,})


def adicionarmembros(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    if request.POST:

        #    url = request.GET.get("next")
        #    try:
        #        resolve(url)
        for username in request.POST.getlist('user'):
            mg = MembroGrupo(account=Account.objects.get(username=username), grupo=grupo, is_admin=False)
            mg.save()

        return HttpResponseRedirect(reverse('grupo_view', kwargs={"grupo_id": grupo_id}))
    else:
        membros = MembroGrupo.objects.filter(grupo_id=grupo_id)
        users = Account.objects.exclude(id=request.user.id)
        for membro in membros:
            users = users.exclude(id=membro.account_id)

        #    url = request.GET.get("next")
        return render(request, 'quarantine/adicionarmembros.html', {'grupo': grupo, 'users': users, })


# def removermembrospage(request, grupo_id):
# grupo = get_object_or_404(Grupo, pk=grupo_id)
# users = grupo.membros.all()

#    url = request.GET.get("next")
# return render(request, 'quarantine/removermembros.html', {'grupo': grupo, 'users': users,
# 'next': url
#                                                              })


def removermembros(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    if request.POST:

        for username in request.POST.getlist('user'):
            mg = MembroGrupo.objects.get(account=Account.objects.get(username=username), grupo=grupo)
            mg.delete()
        return HttpResponseRedirect(reverse('grupo_view', kwargs={'grupo_id': grupo_id}))
    else:
        users = grupo.membros.all().exclude(id=request.user.id)

        #    url = request.GET.get("next")
        return render(request, 'quarantine/removermembros.html', {'grupo': grupo, 'users': users,
                                                                  # 'next': url
                                                                  })


def sairgrupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    user = request.user
    grupo.membros.remove(user)
    print(is_admin(request, grupo_id))
    if not MembroGrupo.objects.filter(grupo_id=grupo):
        grupo.delete()
    return HttpResponseRedirect(reverse('menu'))


# ----------------------------------------------------------------------


def publicacao(request, grupo_id, pub_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    pub = get_object_or_404(Publicacao, pk=pub_id)
    candeletepub = is_admin(request, grupo_id) or pub.autor.id == request.user.id
    comentarios = Comentario.objects.filter(publicacao_id=pub_id).order_by('-karma', 'pub_data')
    return render(request, 'quarantine/publicacao.html',
                  {'grupo': grupo, 'pub': pub, 'comentarios': comentarios, 'candeletepub': candeletepub})


def juntaragrupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    user = request.user
    if grupo.publico or request.user.is_admin:
        try:
            membro = get_object_or_404(MembroGrupo, grupo_id=grupo_id, account_id=user.id)
        except(KeyError, Http404):
            membro = MembroGrupo(grupo=grupo, account=user)
            membro.save()
            return grupo_view(request, grupo_id)
        else:
            return grupo_view(request, grupo_id)


# def publicacoesgrupo(request, grupo_id):
#     grupo = get_object_or_404(Grupo, pk=grupo_id)
#     if(request.user.is_admin | request.user is in grupo.membros | grupo.publico):
#         pubs = Publicacao.Objects.filter(grupo=grupo)
#
#     return render(request, 'quarantine/grupo.html', {'grupo': grupo, 'pubs': pubs, 'candeletepub': candeletepub})


def publicarcomentario(request, grupo_id, pub_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    pub = get_object_or_404(Publicacao, pk=pub_id)
    url = request.GET.get("next")
    try:
        resolve(url)

        com = Comentario(conteudo=request.POST['conteudo'], pub_data=timezone.now(), karma=0, autor=request.user,
                         publicacao=pub)
        com.save()
        # return HttpResponseRedirect(reverse('publicacao', args=(grupo_id, pub_id)))
        return HttpResponseRedirect(url)
    except (KeyError, Resolver404):
        return HttpResponseRedirect(reverse('menu'))


def apagarcomentario(request, grupo_id, pub_id, com_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    pub = get_object_or_404(Publicacao, pk=pub_id)
    com = get_object_or_404(Comentario, pk=com_id)

    candeletepub = MembroGrupo.objects.get(grupo_id=grupo_id, account_id=request.user.id).is_admin or \
                   pub.autor.id == request.user.id
    candeletecom = MembroGrupo.objects.get(grupo_id=grupo_id, account_id=request.user.id).is_admin or \
                   com.autor.id == request.user.id

    if candeletecom:
        com.delete()
        # return publicacao(request, grupo_id, pub_id)
        # return render(request, 'quarantine/publicacao.html', {'grupo': grupo, 'pub': pub, 'candeletepub': candeletepub})
        return HttpResponseRedirect(reverse('publicacao', kwargs={'grupo_id': grupo_id, 'pub_id': pub_id}))
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
