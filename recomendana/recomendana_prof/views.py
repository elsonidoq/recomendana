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
	#return render_to_response("voting/vote.html", context_instance=RequestContext(request))
    account = request.user.account
    # ESTE ESTILO NO SE USA PERO QUEDA COPAAAADO!
    s = """
<html>
<style>
body {
background-color: black;
color: white;
font-size: 10pt;
font-family: Arial, Verdana;
}
table {
font-size: 10pt;
}
img {
//border: 1px solid white;
}
h2 {
padding: 0px 0px 0px 0px;
margin: 0px 0px 0px 0px;
}
hr {
color: white;
background-color: white;
border: 0px solid white;
height: 1px;
margin: 0px;
padding: 0px;
}
hr.inter {
color: #505050;
background-color: #505050;
border: 0px solid #505050;
height: 1px;
}

</style>
<body><center>
"""

    # EL ESTILO DE ARRIBA NO SE USA PERO QUEDA COPAAADO

    s = ""
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
                #account.set_vote(v[0], )
            elif v[1] == "t":
                last_seen= request.POST[vot]
                #account.set_time(v[0], request.POST[vot])
            if mid is not None and vote is not None and last_seen is not None:
                account.vote(mid, vote, last_seen)
                mid= None 
                vote= None
                last_seen=None
        except:
            pass
        


    s += "<div style='width:800px;text-align:left'>"
    s += "Bienvenido " + request.user.username + "! "
    s+= "(<a href='./logout/'>Logout</a>)<br/>"
    s += "Ya has votado " + str(account.get_votes_count()) + " pel&iacute;culas y nos dijiste que no has visto " + str(account.get_unseen_count()) + "<br/>"
    s += "</div>"

    s += "<br/>"


    s += "<div style='text-align:left; width: 800px;'>"
    s += "<form action='' method='GET'>"
    s += "Buscar pel&iacute;cula: "
    query_value = request.GET["query"] if "query" in request.GET.keys() else ""
    query_value = query_value.replace("'", "\'")
    s += "<input type='text' name='query' style='width:300px;' value='" + query_value + "'>"
    s += "<input type='submit' value='buscar'>"
    s += "</form>"
    s += "</div>"

    if "query" in request.GET.keys():
        ms = account.get_movies_by_query(request.GET["query"])
        if len(list(ms)) == 0:
            s += "No se han encontrado resultados<br/><br/><hr/><br/>"
            ms = account.get_movies_to_review(5)
    else:
        ms = account.get_movies_to_review(5)
        print ms

    s += "<form action='./?uid=" + "uid" + "' method='POST'>"
    s += "<table style='width:800px;'>"
    for m in ms:
        s += "<tr>"
        s += "<td style='width:100px;vertical-align:top;'><img src='" + m.image.replace('www','sc') + "' width='100px'/><br/><br/></td>"

        s += "<td style='padding-left: 10px;'>"
        
        s += "<h3>" + m.title + "</h3><hr class='inter'/>"
        s += "Cast: " + m.cast + "<br/>"
        s += "Director: " + m.director + "<br/>"
        s += "Year: FALTA IMPORTAR<br/>"# + int(m.year) + "<br/>"
        s += "Genre: " + str(m.genre) + "<br/>"
        s += "Plot: " + m.description + "<br/>"

        s += "<br/>"
        s += "Puntaje: "
        dvote = dict()
        dvote["0"] = "No la he visto"
        for i in xrange(1,6):
            dvote[str(i)] = str(i)
        ks = dvote.keys()
        ks.sort()
        for k in ks:
            sel = "checked" if account.get_vote(m.id) == int(k) else ""
            s += "<input type='radio' " + sel + " name='" + str(m.id) + "_n' value='" + k + "'/> " + dvote[k]
        s += "<br/>"

        s += "La vi hace: "
        dtime = dict()
        dtime["0"] = "M&aacute;s de 10 a&ntilde;os"
        dtime["1"] = "Menos de 10 a&ntilde;os"
        dtime["2"] = "Menos de 5 a&ntilde;os"
        dtime["3"] = "Recientemente"
        ks = dtime.keys()
        ks.sort()
        for k in ks:
            sel = "checked" if account.get_time(m.id) == int(k) else ""
            s += "<input type='radio' " + sel + " name='" + str(m.id) + "_t' value='" + k + "'/> " + dtime[k]
        
        s += "</td></tr>"

        s += "<tr><td colspan='2'><hr></td></tr>"

    s += "</table>"
    s += "<input type='submit' value='Votar y 5 m&aacute;s'>"
    s += "</form>"
    return HttpResponse(s)

def index(request):
    if request.user.is_authenticated():
        return voting(request)
    return render_to_response("index.html", context_instance=RequestContext(request))
