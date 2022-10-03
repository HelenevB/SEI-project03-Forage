from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
     path('about/', views.about, name='about'),
   
     # image urls 

    path('images/', views.image_Index, name='image_Index'),
    path('images/<int:image_id>', views.images_detail, name='detail'),
    path('images/create/', views.ImageCreate.as_view(), name='images_create'),
    path('images/<int:pk>/update/', views.ImageUpdate.as_view(), name='images_update'),
    path('images/<int:pk>/delete/', views.ImageDelete.as_view(), name='images_delete'),
    path('images/<int:image_id>/add_to_board/', views.add_to_board, name='add_to_board'),











     # userprofile urls 
     path('users/<int:user_id>/', views.profile_detail, name='profile_detail'),
     # path('users/<int:user_id>/update', views.profile_update, name='profile_update'),
     # path('users/<int:user_id>/delete', views.profile_delete, name='profile_delete'),

     

    # authenitcation urls 








     # board urls 



    






]