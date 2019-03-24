    
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addUser/', views.add_user_view, name='addUser'),
    path('<int:id>/', views.public_images_view, name='publicImages'),
    path('login/', views.login, name='login'),
    path('edit/<int:id>/', views.update_user, name='updateUser'),
    path('editPublic/', views.edit_public, name='editPublic'),
]