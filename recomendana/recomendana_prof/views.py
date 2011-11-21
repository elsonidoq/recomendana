from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from recomendana_prof.forms import NamedRegForm,AnonRegForm
from django.contrib.auth import logout

def anonregister(request):
    form = AnonRegForm()
    
    return render_to_response('registration/anonymous.html', {'anonreg_form': form},context_instance=RequestContext(request))
    
    
def namedregister(request):
    if request.user.is_authenticated():    
        return render_to_response("index.html", context_instance=RequestContext(request))
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
        
def index(request):
    return render_to_response("index.html", context_instance=RequestContext(request))