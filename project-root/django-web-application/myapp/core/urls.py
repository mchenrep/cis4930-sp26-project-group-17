from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('repos/', views.repo_list, name='repo_list'),
    path('repos/add/', views.repo_create, name='repo_create'),
    path('repos/<int:pk>/', views.repo_detail, name='repo_detail'),
    path('repos/<int:pk>/edit/', views.repo_edit, name='repo_edit'),
    path('repos/<int:pk>/delete/', views.repo_delete, name='repo_delete'),
    path('analytics/', views.analytics, name='analytics'),
]

path('fetch/', views.trigger_fetch, name='trigger_fetch')