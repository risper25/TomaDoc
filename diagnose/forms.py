from django import forms
from .models import *
from django.contrib.auth.models import User
DISEASE_CHOICES = (('all','all'),
    ('Tomato mossaic virus','Tomato mossaic virus'),
    ('Tomato yellow leaf curl virus', 'Tomato yellow leaf curl virus'),
    ('Tomato target spot', 'Tomato target spot'),
    ('Tomato spider mites', 'Tomato spider mites'),
     ('Tomato septoira leaf spot', 'Tomato septoira leaf spot'),
      ('Tomato leaf mold', 'Tomato leaf mold'),
       ('Tomato late blight', 'Tomato late blight'),
       ('Tomato early blight', 'Tomato early blight'),
       ('Tomato bacterial spot', 'Tomato bacterial spot'))
class imageForm(forms.ModelForm):
         
    class Meta:
        model = ImageModel
        fields = ('imagefile',)
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=('comment',)
        
class userdetailsForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username','email',)
            
                        
class profileForm(forms.ModelForm):
	class Meta:
	    model = Profile
	    fields = ('imagefile',)  


class pestisideForm(forms.ModelForm):
    choices = forms.ModelChoiceField(queryset=Disease.objects.all())
    class Meta:
        model = Pestiside
        fields = ('name','imagefile','directions','price')
        

class FilterForm(forms.Form):
    #selectedplant = forms.ModelChoiceField(queryset=Disease.objects.all(), required=True)
    selected= forms.CharField(label='Filter by disease', widget=forms.Select(choices=DISEASE_CHOICES))

class diseaseForm(forms.ModelForm):
    model=Disease
    fields=('symptoms',)

    

