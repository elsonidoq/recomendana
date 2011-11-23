from django import forms
from django.core import validators
from django.contrib.auth.models import User
from datetime import date
import uuid

class AnonRegForm(forms.Form):
    name = forms.RegexField(regex=r'^\w+$',   widget=forms.TextInput(), required=False )
    dob = forms.DateField(widget=forms.DateInput(attrs={'class':'datePicker', 'readonly':'true'}), label=u'Fecha de nacimiento', required=False)
    film_exp = forms.ChoiceField(initial='0', label=u'Experiencia filmica(?)', required=False,
                                 choices = (('0','Que te importa'),  ('1','Principiante'),('2','Decente'),('3','Una vez vi una peli japonesa'),('4','Intermedio'),('5','Avanzado')))
    sexo = forms.ChoiceField(required=False, initial='', choices = (('','Que te importa'), ('True','Masculino'),('False','Femenino')), label=u'Sexo')

    def habemusUsername(self):
        return 'name' in self.cleaned_data and len(self.cleaned_data['name'])>0 and not self.cleaned_data['name'].isspace()

    def clean(self):
        if self.habemusUsername():
            try:
                u = User.objects.get(username=self.cleaned_data['name'])
                if u != None:                    
                    msg = u'Usuario ya existe'
                    self._errors["name"] = self.error_class([msg])
                    raise forms.ValidationError(msg)
            except User.DoesNotExist:
                pass
        
        if 'dob' in self.cleaned_data and self.cleaned_data['dob'] != None and self.cleaned_data['dob'] > date (2000,1,1):
            msg = u'Volve en un par de anios.'
            self._errors["dob"] = self.error_class([msg])
            raise forms.ValidationError(msg)
            
        return self.cleaned_data
    
    def save(self, new_data,meta):
        if self.habemusUsername():
            username = new_data['name']
        else:
            username = "anon"+ str(uuid.uuid1())[0:20]
        u = User.objects.create_user(username,
                                     "anon@"+str(uuid.uuid1())+".org",
                                     str(uuid.uuid1()))
        u.is_active = False
        u.save()
        
        u.get_profile().is_anonymous = True
        print new_data["dob"]
        if new_data["dob"]!=None:
            u.get_profile().birth_date = new_data["dob"]
        if int(new_data["film_exp"]) > 0:
            u.get_profile().film_experience = int(new_data['film_exp'])
        if not new_data["sexo"].isspace():
            u.get_profile().gender = bool(new_data['sexo'])
        u.get_profile().access_ip = meta['REMOTE_ADDR']
        u.get_profile().save()

        return u
    
class NamedRegForm(forms.Form):
    name = forms.RegexField(regex=r'^\w+$',   widget=forms.TextInput(),required=True,label=u'Nombre de usuario' )
    dob = forms.DateField(widget=forms.DateInput(attrs={'class':'datePicker', 'readonly':'true'}), label=u'Fecha de nacimiento', required=True)
    email = forms.EmailField(required=True, label=u'Direccion de email')
    film_exp = forms.ChoiceField(required=True, initial='1', label=u'Experiencia filmica(?)',
                                 choices = (('1','Principiante'),('2','Decente'),('3','Una vez vi una peli japonesa'),('4','Intermedio'),('5','Avanzado')))
    sexo = forms.ChoiceField(required=True, initial='True', choices = (('True','Masculino'),('False','Femenino')), label=u'Sexo')
    password_orig = forms.CharField(widget=forms.PasswordInput(), label=u'Password', required=True)
    password_rep = forms.CharField(widget=forms.PasswordInput(), label=u'Password (otra vez)', required=True)
    
    def hayField(self, f):
        return f in self.cleaned_data and len(self.cleaned_data[f])>0 and not self.cleaned_data[f].isspace()


    def clean(self):
        if 'password_orig' in self.cleaned_data and 'password_rep' in self.cleaned_data:
            if self.cleaned_data['password_orig'] != self.cleaned_data['password_rep']:
                # no se si esta bueno acceder a _errors
                msg = u'Passwords diferentes'
                self._errors["password_rep"] = self.error_class([msg])
                raise forms.ValidationError(msg)
        
        if self.hayField('name'):
            try:
                u = User.objects.get(username=self.cleaned_data['name'])
                if u != None:                    
                    msg = u'Usuario ya existe'
                    self._errors["name"] = self.error_class([msg])
                    raise forms.ValidationError(msg)
            except User.DoesNotExist:
                pass
        
        if self.hayField('email'):
            try:
                u = User.objects.filter(email=self.cleaned_data['email'])
                if len(u)>0:
                    msg = u'Email ya existe'
                    self._errors["email"] = self.error_class([msg])
                    raise forms.ValidationError(msg)
            except Exception as e:
                raise forms.ValidationError(e)
            
        if 'dob' in self.cleaned_data and self.cleaned_data['dob'] > date (2000,1,1):
            msg = u'Volve en un par de anios.'
            self._errors["dob"] = self.error_class([msg])
            raise forms.ValidationError(msg)
            
        return self.cleaned_data
    
    def save(self, new_data,meta):
        u = User.objects.create_user(new_data['name'],
                                     new_data['email'],
                                     new_data['password_orig'])
        
        #TODO, poner un hash y hacer que lo devuelvan antes de activarlos
        u.is_active = False
        u.save()
        
        u.get_profile().is_anonymous = False
        u.get_profile().birth_date = new_data["dob"]
        u.get_profile().film_experience = int(new_data['film_exp'])
        u.get_profile().gender = bool(new_data['sexo'])
        u.get_profile().access_ip = meta['REMOTE_ADDR']
        
        u.get_profile().save()
        
        u.get_profile().mandarconfirm()
        
        return u