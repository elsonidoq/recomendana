
# -*- coding: latin-1 -*-
from django.shortcuts import render_to_response,redirect
from django.template.loader import render_to_string
from django.template import RequestContext, Template

from recomendana_prof.forms import NamedRegForm,AnonRegForm
from recomendana_prof.models import ConfirmManager, Movie, Account

from django.contrib.auth import logout,load_backend, login
from django.contrib.auth.models import User
from django.conf import settings
 
from django.core.urlresolvers import reverse, NoReverseMatch

from django.http import HttpResponse

 
def confirmregister(request, key):
    user = None
    manager = ConfirmManager()

    if key == None:
        if request.method == 'POST' and 'key' in request.POST:
            key = request.POST['key'].strip()

    if key != None:
        key = key.lower()
        user = manager.confirm_email(key)
        
    values = {'key': key}
    if user != None:
        values['user_confirmacion'] = user
        values['next'] = reverse("django.contrib.auth.views.login")
    
    return render_to_response("registration/confirm.html",
                values, context_instance=RequestContext(request))
    
def anonregister(request):
    if request.user.is_authenticated():    
        return redirect('/')
    form = None
    if request.method == 'POST':
        form = AnonRegForm(request.POST)
        if form.is_valid():
            u = form.save(form.cleaned_data, request.META)
           
            for backend in settings.AUTHENTICATION_BACKENDS:
                if u == load_backend(backend).get_user(u.pk):
                    u.backend = backend
            if hasattr(u, 'backend'):
                 login(request, u)
                 
            return redirect('/')
    else:
        form = AnonRegForm()
    
    return render_to_response('registration/anonymous.html', {'anonreg_form': form}, context_instance=RequestContext(request))
    
    
def namedregister(request):
    if request.user.is_authenticated():
        #TODO, con el nombre de la vista no anda.
        return redirect('/')
    form = None
    success = False
    if request.method == 'POST':
        form = NamedRegForm(request.POST)
        if form.is_valid():
            u = form.save(form.cleaned_data, request.META)
            success = True
    else:
        form = NamedRegForm()
    
    return render_to_response('registration/register.html', {'namedreg_form': form, 'success': success}, context_instance=RequestContext(request))
    
    
def salir(request):
    logout(request)
    return redirect('/')

def voting(request):
    if not request.user.is_authenticated():
        #TODO, con el nombre de la vista no anda.
        return redirect('/')
    print request.POST
    account = request.user.account
    search_msg = None
    mid= None 
    vote= None
    last_seen=None
    for vot in request.POST.keys():
        v = []
        if "_" in vot:
            v = vot.split("_")
        try:
            v[0] = int(v[0])

            if v[1] == "n":
                vote= request.POST[vot]
                mid= v[0]

            elif v[1] == "t":
                last_seen= request.POST[vot]

            if vote is not None and last_seen is None:
                last_seen = 0

            if mid is not None and vote is not None and last_seen is not None:
                account.vote(mid, vote, last_seen)
                mid= None 
                vote= None
                last_seen=None
        except:
            pass
    
  
    query_value = request.GET["query"] if "query" in request.GET.keys() else None
   
    if query_value is not None:
        ms = account.get_movies_by_query(query_value)
        if len(list(ms)) == 0:
            search_msg = "No se han encontrado resultados"
            ms = account.get_movies_to_review(5)
    else:
        ms = account.get_movies_to_review(5)


    voto_previo = {}
    dtime_previo = {}
    movies = list(ms)
        
    for m in movies:
        # esto puede pasar?
        voto_previo[m.id] = account.get_vote(m.id)
        dtime_previo[m.id] = account.get_time(m.id)
        # esto deberia arreglarse con un script a la base o antes de importar
        m.image = m.image.replace('www','sc')
        
    return render_to_response("voting/vote.html", {'movies': movies, 'voto_previo': voto_previo,'query_value': query_value,
                                                   'dtime': dictParaReferenciaTemporal(), 'dtime_previo': dtime_previo,
                                                   'search_msg': search_msg},
                             context_instance=RequestContext(request))
 
def dictParaReferenciaTemporal():
    dtime = {}
    dtime[1] = "Más de 10 años"
    dtime[2] = "Menos de 10 años"
    dtime[3] = "Menos de 5 años"
    dtime[4] = "Recientemente"
    return dtime

def index(request):
    #if request.user.is_authenticated():
    #    return voting(request)
    return render_to_response("index.html", context_instance=RequestContext(request))
