from django.db.models import Count, Sum
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .forms import ItemForm
from .models import Item

class HomeView(TemplateView):
    template_name = "myapp/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item_count"] = Item.objects.count()
        return context

class ItemListView(ListView):
    model = Item
    template_name = "myapp/list.html"
    context_object_name = "items"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

class ItemDetailView(DetailView):
    model = Item
    template_name = "myapp/detail.html"
    context_object_name = "item"

class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = "myapp/form.html"

class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = "myapp/form.html"

class ItemDeleteView(DeleteView):
    model = Item
    template_name = "myapp/confirm_delete.html"
    success_url = reverse_lazy("item_list")

class AnalyticsView(TemplateView):
    template_name = "myapp/analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = Item.objects.count()
        context["total_value"] = Item.objects.aggregate(total=Sum("value"))["total"] or 0
        context["categories"] = Item.objects.values("category").annotate(count=Count("id")).order_by("category")
        return context
