from django.db import models
from django.contrib.auth import authenticate,get_user_model
from datetime import datetime
from django.db.models.signals import post_save

from django.dispatch import receiver



# Create your models here
User=get_user_model()


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    imagefile =models.ImageField(upload_to='profile/',default='user.png')
    def __str__(self):
        return str(self.imagefile)
'''
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        #instance.profile.save()'''


class ImageModel(models.Model):
    imagefile=models.ImageField(upload_to='pestisides/', null=True, verbose_name="")
    
    #result=models.CharField(max_length=100,choices=DISEASE_CHOICES ,default='tomato early blight')

    def __str__(self):
        return str(self.imagefile)



class Disease(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=50000)
    symptoms=models.CharField(max_length=50000,default="symptom1.symptom2")
    #imagefile=models.ImageField(upload_to='pestisides/', null=True, verbose_name="")
    #prevention=models.CharField(max_length=50000,default="symptom1.symptom2")

    
    def __str__(self):
        return self.name




class Pestiside(models.Model):
    name=models.CharField(max_length=100)
    imagefile=models.ImageField(upload_to='pestiside/', null=True, verbose_name="")
    directions=models.CharField(max_length=50000)
    #image
    price = models.CharField(max_length=100)
    disease = models.ManyToManyField(Disease)
    #test_location=
    #time
    def __str__(self):
        return self.name
                        

class Prediction(models.Model):
    image= models.OneToOneField(ImageModel,on_delete=models.CASCADE,null=True)
    user= models.ForeignKey(User,default=1, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease,on_delete=models.CASCADE)
    time= models.DateTimeField(auto_now_add=True, blank=True)
    
   
class Review(models.Model):
    
  author= models.ForeignKey(User,default=1, on_delete=models.CASCADE)
  time = models.DateTimeField(auto_now_add=True, blank=True)
  pes = models.ForeignKey(Pestiside,default=0,on_delete=models.CASCADE)
  comment = models.CharField(max_length=200)
  