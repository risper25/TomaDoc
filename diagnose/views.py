from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.generic.edit import DeleteView,FormView
from django.views.generic import ListView
from django.views import View
from django.shortcuts import get_object_or_404
from .forms import *
from .models import *
from .py_templates.my_model import *
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
# Create your views here.

#@method_decorator(login_required, name='dispatch')
class upload(LoginRequiredMixin,View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        prediction=None
        image=None
        form=imageForm()
        pestisides=None
        disease=None
        
        context={'form':form,'image':image,'disease':disease,'pestisides':pestisides}
        return render(request,'diagnose/predict.html',context)
    def post(self,request):
        user = User.objects.get(username=request.user)

        if request.method == 'POST':
            form=imageForm(request.POST,request.FILES)
            if form.is_valid():
               form.save()
               #pass image to the model
               prediction=Prediction.objects.last()
               img=ImageModel.objects.last()
       
               
               #print(now)
               print(img)
               
               url= img.imagefile
               top_p,top_class=image_pred(url)
               # out=dis[int(out)]
               print('----------------',url,'----------------')
               #print('-----disease is------- ',out,'----------')
               disease_map={0:'Tomato bacterial spot',1:'Tomato early blight',2:'Tomato late blight',3:'Tomato leaf mold',
               4:'Tomato septoira leaf spot',5:'Tomato spider mites',
               6:'Tomato target spot',7:'Tomato yellow leaf curl virus',
               8:'Tomato mossaic virus',
               9:'this is a healthy tomato',10:'Please upload a picture of a tomato leaf'}
               
        
               print(top_class)
               
               disease=None
               
               if top_class != 10:
                background=False
                disease=get_object_or_404(Disease,name=disease_map[top_class])
                new_prediction=Prediction()
                new_prediction.user=user
                new_prediction.image=img
                new_prediction.disease=disease
                new_prediction.save()
               else:
                background=True
                os.remove(os.path.join(settings.MEDIA_ROOT, str(url)))
                img.delete()
                   

               pestisides=Pestiside.objects.filter(disease=disease)
               context={'form':form,'image':img,'disease':disease,'pestisides':pestisides,'background':background}    
               return render(request,'diagnose/predict.html',context)

'''
class save_prediction(View):
   def get(self,request):
        user = User.objects.get(username=request.user)
        image=ImageModel.objects.last()
        disease=Disease.objects.get(name=image.result)
        new_prediction=Prediction()
        new_prediction.user=user
        new_prediction.disease=disease
        new_prediction.save()
        return render(request,'diagnose/predict.html')  
        '''  
    
class upload_profile(View):

    def post(self,request):
        user=request.user
        u_form=userdetailsForm(request.POST,instance=request.user)
        p_form=profileForm(request.POST,request.FILES,instance=request.user.profile)
    
        if u_form.is_valid() and p_form.is_valid():
            
               u_form.save()
               p_form.save()
            
               
               
               return redirect('diagnose:predictions')

    def get(self,request):
        
        u_form=userdetailsForm(instance=request.user)
        p_form=profileForm(instance=request.user.profile)
        return render(request,'diagnose/userprofile.html',{'u_form':u_form,'p_form':p_form})

class view_profile(View):
    def get(self,request):
        
        
        profile = Profile.objects.get_or_create(user=request.user)

        
        userprofile=profile.user
        prediction_info= Prediction.objects.filter(user=user)
        predictions=prediction_info.count()
        context={'user':userprofile,'predictions':predictions}
        return render(request,'diagnose/viewuserprofile.html',context)

class view_dashprofile(View):
    def get(self,request,*args,**kwargs):
        id_p = self.kwargs.get("id")
        
        profile=get_object_or_404(Profile,user__id=id_p)
        userprofile=profile.user
        prediction_info= Prediction.objects.filter(user=user)
        predictions=prediction_info.count()
        context={'user':userprofile,'predictions':predictions}
        return render(request,'diagnose/viewuserprofile.html',context)
     

#prediction list views
class predictions(View):


    def get(self,request):
        user = request.user
    
        
        prediction_info=Prediction.objects.filter(user=user).order_by('time').reverse()
        isadmin=False
        if user.username == 'admin':
            isadmin=True;
        else:
            isadmin=False;
     
        totals=prediction_info.count()
        diseases=[p.disease for p in prediction_info]
        image=[p.image for p in prediction_info]
        disease_list=set(diseases)
        pestisides=Pestiside.objects.all()
        suggestions=[Pestiside.objects.filter(disease__name=d.name) for d in diseases]
        #print(diseases)
        #print(suggestions)
        form = FilterForm() 
        context={'diseases': diseases,'form': form,'disease_list':disease_list,'images':image,'sugestions':suggestions,'predictions':prediction_info,'total':totals,'user':user,'admin':isadmin}
        return render(request,'diagnose/userbase.html',context)
    def post(self,request):
        if request.method=='POST':
            user = User.objects.get(username=request.user)
            profile=get_object_or_404(Profile,user=user)
            diseases=Disease.objects.all()
            form = FilterForm(request.POST) 
            if form.is_valid():
                print('sucessfull')
                selectedplant = form.cleaned_data['selected']
                if selectedplant == 'all':
                    predictions=Prediction.objects.filter(user=user)
                else:    
                    predictions = Prediction.objects.filter(user=user,disease__name=selectedplant)
                number=predictions.count()

                
            else:
                print('not')
                predictions = Prediction.objects.all().order_by('time')  
        else:
            predictions = Prediction.objects.all().order_by('time')    

        context =  {'predictions':predictions,'number':number,'profile':profile, 'form': form,'diseases':diseases}
        return render(request,'diagnose/userbase.html',context)

class prediction(View):
    template_name='diagnose/prediction.html'
    def get(self,request,*args,**kwargs):
        pk=self.kwargs.get("pk")
        prediction=get_object_or_404(Prediction,pk=pk)
        disease=prediction.disease
        if disease.name == 'this is a healthy tomato':
            healthy=True
        else:
            healthy=False    

        disease=prediction.disease
        pestisides=Pestiside.objects.filter(disease=disease.pk)

        image=prediction.image
        print(disease)
        print(pestisides)
        symptoms=disease.symptoms
        symptoms=symptoms.split(".")
          
        context={'prediction':prediction,'healthy':healthy,'disease':disease,'pestisides':pestisides,'image':image,"symptoms":symptoms}
        return render(request,self.template_name,context)
    



class delete_prediction(DeleteView):
    template_name='diagnose/predictions_delete.html'
    def get_object(self):
        id_=self.kwargs.get("id")
        return get_object_or_404(Prediction,id=id_)
    
    def get_success_url(self):
        return reverse('diagnose:predictions')
    
           
'''
def filter_predictions(request):
    user = User.objects.get(username=request.user)
    diseases=Disease.objects.all()
    form = FilterForm()
    sightings = []
    if request.POST:
        form = FilterForm(request.POST)
        if form.is_valid():
            print('sucessfull')
            selectedplant = form.cleaned_data['selectedplant']
            print(selectedplant)
            predictions = Prediction.objects.filter(disease=selectedplant)
            for p in predictions:
                print(p.time)
        else:
            print('not')
            predictions = Prediction.objects.all().order_by('time')  
    else:
        predictions = Prediction.objects.all().order_by('time')    

    context =  {'predictions':predictions, 'form': form,'diseases':diseases}
    return render(request,'diagnose/userbase.html',context)
'''

class review(View):
    template_name='diagnose/review.html'
    reviews= Review.objects.all().order_by('comment')
    
    def get(self,request):
        form= ReviewForm()
        self.user=None
        context={'form':form,'reviews':self.reviews,'user':self.user}
        return render(request,template_name,context)  
    def post(self,request):
        if request.method=='POST':
            user = User.objects.get(username=request.user)
            form= ReviewForm(request.POST)
            if form.is_valid():
                final_form=form(commit=False)
                final_form.save()
                comment=form.cleaned_data.get('review')
                new_review=Review.objects.create(author=user,comment=comment)
                new_review.save()
            return redirect('diagnose:review')    
'''  
class delete_review(View):
    def post():
'''

class Pestisides(FormView):
    form_class = ReviewForm
    def get(self,request,*args,**kwargs):
        pk=self.kwargs.get("pk")
        di = self.kwargs.get("di")
        dis=get_object_or_404(Disease,pk=di)
        pestiside=get_object_or_404(Pestiside,pk=pk)
        display=True
        reviews= Review.objects.filter(pes=pestiside).order_by('time').reverse()
        form= ReviewForm()
        self.user=None
        current_user=request.user
        context={'pestiside':pestiside,'form':form,'reviews':reviews,'user':self.user,'current_user':current_user,'display':display}
        return render(request,'diagnose/pestiside.html',context)  
    
        '''  def post(self,request,*args,**kwargs):
          pk = self.kwargs['pk']
          di = self.kwargs['di']
          pestiside=get_object_or_404(Pestiside, pk=pk, disease__id=di)
          user = request.user
          form= ReviewForm(request.POST)
          if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.pes = pestiside
            form.save() 
            return redirect('diagnose:pestiside')'''
        '''def form_valid(self, form):

            # you will need to make your view a FormView and define a form_class variable with ReviewForm
            review = form.save(commit=False)

            pk = self.kwargs.get("pk")
            di = self.kwargs.get("di")
            dis = get_object_or_404(Disease,pk=di)
            pestiside = Pestiside.objects.get(pk=pk, disease=dis)

            review.author = self.request.user
            review.pes = pestiside
            review.save()
            return redirect('diagnose:pestiside')    '''


#form view
class CommentView(FormView):
    template_name = 'pestiside.html'
    form_class = ReviewForm
    #success_url = '/succsess/'
    pk_url_kwarg ='pestiside_id'
    di_url_kwarg ='disease_id'

    def form_valid(self, form): 
        review = form.save(commit=False)

        pk = self.kwargs.get("pk")
        di = self.kwargs.get("di")
        dis = get_object_or_404(Disease,pk=di)
        pestiside = Pestiside.objects.get(pk=pk, disease=dis)

        review.author = self.request.user
        review.pes = pestiside
        review.save()

    def get_success_url(self):
        return reverse('diagnose:pestiside',kwargs={'pestiside_id':self.object.id,'disease_id':self.object.id})    
      
       


class delete_review(DeleteView):
    template_name='diagnose/review_delete.html'
    pk_url_kwarg ='pestiside_id'
    di_url_kwarg ='disease_id'
    def get_object(self):
        id_=self.kwargs.get("id")
        return get_object_or_404(Review,id=id_)
    
    def get_success_url(self):
        return reverse('diagnose:pestiside',kwargs={'pestiside_id':self.object.id,'disease_id':self.object.id})


############################Admin##################################

class View_usersa(View):
    def get(self,request):
        User=get_user_model()
        users=User.objects.all()
        user = request.user
        total_users=User.objects.all()
        user_predictions=Prediction.objects.filter(user=user)

        disease=Disease.objects.all()
        pestisides=Pestiside.objects.all()
        
        fieldname = 'disease'
        data=Prediction.objects.values(fieldname)
        final_list=[]
        for d in data:
            final_list.append(d['disease'])
        
        final_dict={d.name:final_list.count(d.id) for d in disease}
        id_dict={d.name:d.id for d in disease}
        print(total_users.count())
        context={'disease':disease,'users':users,'id_dict':id_dict,'my_users':total_users,'total':total_users.count(),'pestisides':pestisides,'user_predictions':user_predictions.count()}
        return render(request,'diagnose/dashusers.html',context)

class View_Pestisides(View):
    def get(self,request):
        User=get_user_model()
        user = request.user
        total_users=User.objects.all()
        user_predictions=Prediction.objects.filter(user=user)

        disease=Disease.objects.all()
        pestisides=Pestiside.objects.all()
        
        fieldname = 'disease'
        data=Prediction.objects.values(fieldname)
        final_list=[]
        for d in data:
            final_list.append(d['disease'])
        
        final_dict={d.name:final_list.count(d.id) for d in disease}
        id_dict={d.name:d.id for d in disease}
        print(total_users.count())
        context={'disease':disease,'final_dict':final_dict,'id_dict':id_dict,'my_users':total_users,'total':total_users.count(),'pestisides':pestisides,'user_predictions':user_predictions.count()}
        return render(request,'diagnose/dashpestisides.html',context)

class View_Diseases(View):
    def get(self,request):
        User=get_user_model()
        user = request.user
        total_users=User.objects.all()
        user_predictions=Prediction.objects.filter(user=user)

        disease=Disease.objects.all()
        pestisides=Pestiside.objects.all()
        
        fieldname = 'disease'
        data=Prediction.objects.values(fieldname)
        final_list=[]
        for d in data:
            final_list.append(d['disease'])
        
        final_dict={d.name:final_list.count(d.id) for d in disease}
        id_dict={d.name:d.id for d in disease}
        print(total_users.count())                

    
       
        context={'disease':disease,'final_dict':final_dict,'id_dict':id_dict,'my_users':total_users,'total':total_users.count(),'pestisides':pestisides,'user_predictions':user_predictions.count()}
        return render(request,'diagnose/dashdisease.html',context)

class AddPestiside(View):
    def get(self,request):
        form=pestisideForm()
        diseases=Disease.objects.all()
        return render(request,'diagnose/add_pestiside.html',{'form':form,'diseases':diseases[:2]})

    def post(self, request):
        if request.method == 'POST':
            form = pestisideForm(request.POST,request.FILES)
            print(form.is_valid())
            if form.is_valid():
                
            

                new_pestiside=Pestiside.objects.create()
                new_pestiside.name = form.cleaned_data.get('name')  
                new_pestiside.imagefile= form.cleaned_data.get('imagefile')  
                diseaseName= form.cleaned_data.get('choices') 
                new_disease=get_object_or_404(Disease,name=diseaseName)
                new_pestiside.disease.add(new_disease)
    
                new_pestiside.directions = form.cleaned_data.get('directions')
                new_pestiside.price = form.cleaned_data.get('price')
                new_pestiside.save()
            return redirect('diagnose:add_pestiside')     

class delete_pestiside(DeleteView):
    template_name='diagnose/admindash_delete.html'
    def get_object(self):
        id_=self.kwargs.get("id")
        return get_object_or_404(Pestiside,id=id_)
    
    def get_success_url(self):
        return reverse('diagnose:dashboard')

class update_pestiside(View):
     def get(self,request,*args,**kwargs):
        pk=self.kwargs.get("id")
        pestiside=get_object_or_404(Pestiside,pk=pk)
        form=pestisideForm(instance=pestiside)
        context={'form':form}
        return render(request,'diagnose/add_pestiside.html',context)

     def post(self,request,*args,**kwargs):
        pk=self.kwargs.get("id")
        pestiside=get_object_or_404(Pestiside,pk=pk)
        if request.method == 'POST':
            form= pestisideForm(request.POST,instance=pestiside)
            if form.is_valid():
                form.save()
                
                pestiside.name = form.cleaned_data.get('name')  
                pestiside.imagefile= form.cleaned_data.get('imagefile')  
                diseaseName= form.cleaned_data.get('choices') 
                new_disease=get_object_or_404(Disease,name=diseaseName)
                pestiside.disease.add(new_disease)

                pestiside.directions = form.cleaned_data.get('directions')
                pestiside.price = form.cleaned_data.get('price')
                pestiside.save()
                return redirect('diagnose:dashboard')

class pestiside_details(DeleteView):
   def get(self,request,*args,**kwargs):
    user=request.user
    pk=self.kwargs.get("id")
    pestiside=get_object_or_404(Pestiside,pk=pk)
    display=True
    context={'pestiside':pestiside,'display':display}
    return render(request,'diagnose/pestiside.html',context)

######diseases admin###########
#edit diseases#
class editDisease(View):
    """docstring for viewDisease"""
    def post(self,request):
        user=request.user
        form=diseaseForm(request.POST,instance=request.user)    
        if form.is_valid():
            form.save()
        return redirect('diagnose:dashdisease')

    def get(self,request,*args,**kwargs):
        id=self.kwargs.get("id")
        disease=get_object_or_404(Disease,id=id)
        form=diseaseForm(instance=request.user)
        return render(request,'diagnose/edit.html',{'form':form,'disease':disease})



            