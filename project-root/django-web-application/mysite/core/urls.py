from django.urls import path
from . import views

# URL paths
urlpatterns = [
    path("", views.home, name="home"),
    path("analytics/", views.analytics, name="analytics"),
    path("listview/", views.RepostioryListView.as_view(), name="repo_list"),
    path("list/<int:pk>/", views.RepositoryDetailView.as_view(), name="repo_detail"),
    path("list/create/", views.list_create, name="list_create"),
    path("list/<int:pk>/update/", views.list_update, name="list_update"),
    path("list/<int:pk>/delete/", views.list_delete, name="list_delete"),
]