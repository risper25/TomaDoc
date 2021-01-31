from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ImageModel)
admin.site.register(Disease)
admin.site.register(Review)
admin.site.register(Pestiside)
admin.site.register(Prediction) 
admin.site.register(Profile) 

