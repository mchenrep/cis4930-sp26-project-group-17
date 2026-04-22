from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Repository
from .forms import RepoForm
import pandas as pd

# Define views

def home(request):
    return render(request, "core/home.html")

class RepostioryListView(ListView):
    model = Repository
    template_name = "core/list.html"
    context_object_name = 'repos'

class RepositoryDetailView(DetailView):
    model = Repository
    template_name = "core/detail.html"
    context_object_name = 'repo'

def list_create(request):
    if request.method == "POST":
        form = RepoForm(request.POST)
        if form.is_valid():
            repo = form.save()
            return redirect("repo_detail", pk = repo.pk)
    else:
        # GET
        form = RepoForm()
    return render(request, "core/form.html", {"form": form})

def list_update(request, pk):
    repo = get_object_or_404(Repository, pk=pk)
    if request.method == "POST":
        form = RepoForm(request.POST, instance=repo)
        if form.is_valid():
            form.save()
            return redirect("repo_detail", pk = repo.pk)
    else:
        # GET
        form = RepoForm()
    return render(request, "core/form.html", {"form": form})

def list_delete(request, pk):
    repo = get_object_or_404(Repository, pk=pk)
    if request.method == "POST":
        repo.delete()
        return redirect("repo_list")
    return render(request, "core/confirm_delete.html", {"repo": repo})

def analytics(request):
    # To be implemented
    return render(request, "core/analytics.html")