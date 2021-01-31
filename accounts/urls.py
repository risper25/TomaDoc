from django.urls import path,include
from django.contrib.auth import views as auth_views

from . import views
app_name='accounts'
urlpatterns = [
    path('',views.home,name="home"),
    path('accounts/login/',views.login_view,name='logIn'),
    path('accounts/register/',views.register_view,name='register'),
   path('accounts/logout/',views.logout_view,name='logout'),

   # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registrations/password_reset_form.html'), name='password_reset'),
   # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registrations/password_reset_done.html'), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registrations/password_reset_confirm.html"), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registrations/password_reset_complete.html'), name='password_reset_complete'),      
    ]
