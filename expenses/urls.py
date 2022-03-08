from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.projects_list, name='list'),
    path('add',views.ProjectCreateView.as_view(),name='add'),
    path('<slug:project_slug>', views.project_detail, name='detail'),
]