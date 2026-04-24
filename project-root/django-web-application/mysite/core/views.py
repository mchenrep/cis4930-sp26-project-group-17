from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Repository, NbaStat
from .forms import RepoForm
import json
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
    qs = NbaStat.objects.all().values('player', 'year', 'pts', 'eff', 'ast', 'reb')
    df = pd.DataFrame(list(qs))

    if df.empty:
        return render(request, "core/analytics.html", {"error": "NBA Data not loaded."})

    # League average points over time (via line chart)
    yearly_trend = df.groupby('year')['pts'].mean().round(2)

    # Top 10 Most Efficient Seasons (via bar chart)
    top_10_eff = df.nlargest(10, 'eff')
    top_10_labels = [f"{row['player']} ({row['year']})" for index, row in top_10_eff.iterrows()]
    top_10_values = top_10_eff['eff'].tolist()

    # Summary stats table
    summary_stats = df[['pts', 'ast', 'reb', 'eff']].describe().round(2).to_dict()

    context = {
        'trend_labels': json.dumps(yearly_trend.index.tolist()),
        'trend_values': json.dumps(yearly_trend.values.tolist()),
        'team_labels': json.dumps(top_10_labels), 
        'team_values': json.dumps(top_10_values),
        'summary_stats': summary_stats,
    }
    return render(request, "core/analytics.html", context)