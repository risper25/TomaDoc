
from django.urls import path,include
from . import views
app_name='diagnose'
urlpatterns = [
    path('upload/',views.upload.as_view(),name="upload"),
    path('predictions/',views.predictions.as_view(),name="predictions"),
    path('predictions/<int:id>/',views.delete_prediction.as_view(),name="delete_prediction"),
     path('pestidide/<int:id>/',views.delete_review.as_view(),name="delete_review"),
    #path('predictions/filtered',views.filter_predictions,name="filter_predictions"),
    path('prediction/<int:pk>/',views.prediction.as_view(),name="prediction"),
    path('pestiside/<int:pk>/<int:di>',views.Pestisides.as_view(),name="pestiside"),
    path('pestiside/review/<int:pk>/<int:di>',views.CommentView.as_view(),name="comment"),
    path('review/',views.review.as_view(),name="review"),
     path('profile/',views.upload_profile.as_view(),name="profile"),
     path('viewprofile/',views.view_profile.as_view(),name="view_profile"),
     path('dashboard/viewprofile/<int:id>/',views.view_dashprofile.as_view(),name="view_dashprofile"),
      path('dashboard/users',views.View_usersa.as_view(),name="dashusersa"),
      path('dashboard/diseases',views.View_Diseases.as_view(),name="dashdiseases"),
      path('dashboard/pestisides',views.View_Pestisides.as_view(),name="dashpestisides"),
      path('add_pestiside/',views.AddPestiside.as_view(),name="add_pestiside"),
       path('pestiside/<int:id>/',views.delete_pestiside.as_view(),name="delete_pestiside"),
       path('pestiside_update/<int:id>/',views.update_pestiside.as_view(),name="update_pestiside"),
       path('pestiside_details/<int:id>/',views.pestiside_details.as_view(),name="pestiside_details"),
       path('edit/<int:id>/',views.editDisease.as_view(),name="editDisease"),
   ]

