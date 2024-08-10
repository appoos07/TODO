# todos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('project/new/', views.create_project, name='create_project'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('project/<int:project_pk>/todo/<int:todo_pk>/edit/', views.edit_todo, name='edit_todo'),
    path('project/<int:project_pk>/todo/<int:todo_pk>/delete/', views.delete_todo, name='delete_todo'),
    path('project/<int:project_id>/export_gist/', views.export_gist, name='export_gist'),
    path('accounts/register/', views.register, name='register'), 
]
