from django.urls import path
from .views import (
    HomeView,
    ItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    AnalyticsView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("items/", ItemListView.as_view(), name="item_list"),
    path("items/new/", ItemCreateView.as_view(), name="item_create"),
    path("items/<int:pk>/", ItemDetailView.as_view(), name="item_detail"),
    path("items/<int:pk>/edit/", ItemUpdateView.as_view(), name="item_update"),
    path("items/<int:pk>/delete/", ItemDeleteView.as_view(), name="item_delete"),
    path("analytics/", AnalyticsView.as_view(), name="analytics"),
]
