from django.urls import path
from . import views

# URL paths
urlpatterns = [
    path("/", views.home, name="home"),
    path("/analytics", views.analytics, name="analytics"),
    path("/listview", views.RepostioryListView.as_view(), name="repo_list"),
    path("/list/", ),
    path("/list/create/", views.list_create),
    path("/list/update/", views.list_update),
    path("/list/delete/", views.list_delete),
]