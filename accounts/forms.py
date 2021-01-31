from django import forms
from django.contrib.auth import authenticate,get_user_model
from .models import *

User = get_user_model()

class UserLoginForm(forms.Form):
    """docstring for UserLoginForm"""
    username= forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput)
    

    def clean(self, *args, **kwargs):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            
            if not user.check_password(password):
                raise forms.ValidationError("Incorect password")
            
            if not user.is_active:
                raise forms.ValidationError("This user is not active")
        
        return  super(UserLoginForm,self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    """docstring for UserRegisterForm"""
    email = forms.EmailField(label='Email Address')
    phone_number = forms.CharField(label='Phone number')
    password = forms.CharField(widget=forms.PasswordInput)
   
    class Meta:
        model =User
        fields= ['first_name','last_name','username','email','password','phone_number']
        
    def clean(self, *args, **kwargs):

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        

        """if password != confirm_password:
            raise forms.ValidationError("passwords must match")
        if len(password)<8:
            raise forms.ValidationError("passwords must be more than 8")
            """
        
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("this email is already been used")

        return super(UserRegisterForm, self).clean(*args, **kwargs)