from django.db import models

class Movie(models.Model):
    cast= models.CharField(max_length=500, null=True)
    cuevana_id= models.IntegerField()
    description = models.TextField(null=True)
    director= models.CharField(max_length=500, null=True)
    genre = models.CharField(max_length=200, null=True)
    image= models.CharField(max_length=200, null=True)
    language= models.CharField(max_length=50, null=True)
    popularity= models.IntegerField(null=True)
    producer= models.CharField(max_length=200, null=True)
    subtitles= models.CharField(max_length=200, null=True)
    title= models.CharField(max_length=150)
    url= models.CharField(max_length=150)

class Account(models.Model):
    is_anonymous=models.BooleanField(default=True)
    # todos los campos son nullable porque la cuenta puede ser anonima
    email= models.CharField(max_length=200, null=True)
    password= models.CharField(max_length=200, null=True)
    birth_date= models.DateField(null=True)
    # BooleanField no puede tener nulls, true=hombre, false=mujer
    gender= models.NullBooleanField(null=True) 
    # La idea es que la persona se autoevalue como critico. 
    film_experience= models.IntegerField(null=True)
    # user agent + lo que sea
    access_ip= models.CharField(max_length=10, null=True)
    access_data= models.TextField(null=True)

class MovieReview(models.Model):
    movie= models.ForeignKey(Movie)
    account= models.ForeignKey(Account)
    # estrellitas, -1 == no la vio, 0 a 5 para la evaluacion
    review= models.IntegerField()
    comment= models.TextField()
    # la ultima vez que la vio. 
    last_watched= models.DateField()
    # el nro. de pag y posicion en la que se mostro la pelicula 
    shown_page=models.IntegerField()
    shown_pos=models.IntegerField()
    # fecha y hora del review
    datetime= models.DateTimeField()


