from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

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
    
    def __str__(self):
        return "title=%s" % self.title

class Account(models.Model):
    user = models.OneToOneField(User)
    is_anonymous=models.BooleanField(default=True)
    # todos los campos son nullable porque la cuenta puede ser anonima
    #email= models.CharField(max_length=200, null=True)
    #password= models.CharField(max_length=200, null=True)
    birth_date= models.DateField(null=True)
    # BooleanField no puede tener nulls, true=hombre, false=mujer
    gender= models.NullBooleanField(null=True) 
    # La idea es que la persona se autoevalue como critico. 
    film_experience= models.IntegerField(null=True)
    # user agent + lo que sea
    access_ip= models.CharField(max_length=10, null=True)
    access_data= models.TextField(null=True)

    def __str__(self):
        return 'id=%s, email=%s' % (self.id, str(self.email))

    def get_movies_to_review(self, cnt=10):
        actual_reviews= self.moviereview_set.all()
        banned_ids= [e.movie.id for e in actual_reviews]
        if len(banned_ids) > 0:
            query= """
                select *
                from  `recomendana`.`recomendana_prof_movie` 
                where id not in (%(ids)s)
                order by rand()*popularity desc 
                limit %(cnt)s
            """ % dict(cnt=cnt, ids=','.join(map(str, banned_ids)))
        else:
            query= """
                select *
                from  `recomendana`.`recomendana_prof_movie` 
                order by rand()*popularity desc 
                limit %(cnt)s
            """ % dict(cnt=cnt)

        return Movie.objects.raw(query)

def link_djangouser_to_account(sender, instance, created, **kwargs):  
    if created:  
       profile, created = Account.objects.get_or_create(user=instance)  
    
class MovieReview(models.Model):
    movie= models.ForeignKey(Movie)
    account= models.ForeignKey(Account)
    # estrellitas, -1 == no la vio, 0 a 5 para la evaluacion
    review= models.IntegerField()
    comment= models.TextField(null=True)
    # la ultima vez que la vio. 
    last_watched= models.DateField()
    # el nro. de pag y posicion en la que se mostro la pelicula 
    shown_page=models.IntegerField()
    shown_pos=models.IntegerField()
    # fecha y hora del review
    datetime= models.DateTimeField()

    def __str__(self):
        return 'movie:%s, account= %s, review=%s' % (self.movie, self.account, self.review)


post_save.connect(link_djangouser_to_account, sender=User) 