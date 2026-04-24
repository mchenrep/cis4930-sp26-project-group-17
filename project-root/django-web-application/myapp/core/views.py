import json

import pandas as pd
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Repository, User, Language
from .forms import RepositoryForm


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------
def home(request):
    context = {
        'total_repos': Repository.objects.count(),
        'total_users': User.objects.count(),
        'total_languages': Language.objects.count(),
        'top_repo': Repository.objects.order_by('-stars').first(),
    }
    return render(request, 'core/home.html', context)


# ---------------------------------------------------------------------------
# List + search + pagination
# ---------------------------------------------------------------------------
def repo_list(request):
    qs = Repository.objects.select_related('owner', 'language').all()

    # Search on repo name or owner username
    query = request.GET.get('q', '').strip()
    if query:
        qs = qs.filter(
            Q(repo_name__icontains=query) | Q(owner__username__icontains=query)
        )

    # Filter by language
    language_id = request.GET.get('language', '')
    if language_id:
        qs = qs.filter(language_id=language_id)

    paginator = Paginator(qs, 20)  # rubric: at least 20 per page
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'core/list.html', {
        'page_obj': page_obj,
        'languages': Language.objects.all(),
        'query': query,
    })


# ---------------------------------------------------------------------------
# Detail
# ---------------------------------------------------------------------------
def repo_detail(request, pk):
    repo = get_object_or_404(
        Repository.objects.select_related('owner', 'language'),
        pk=pk,
    )
    return render(request, 'core/detail.html', {'repo': repo})


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
def repo_create(request):
    if request.method == 'POST':
        form = RepositoryForm(request.POST)
        if form.is_valid():
            repo = form.save()
            messages.success(request, f'Created {repo}.')
            return redirect('repo_detail', pk=repo.pk)
    else:
        form = RepositoryForm()
    return render(request, 'core/form.html', {'form': form})


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
def repo_edit(request, pk):
    repo = get_object_or_404(Repository, pk=pk)
    if request.method == 'POST':
        form = RepositoryForm(request.POST, instance=repo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes saved.')
            return redirect('repo_detail', pk=repo.pk)
    else:
        form = RepositoryForm(instance=repo)
    return render(request, 'core/form.html', {'form': form})


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
def repo_delete(request, pk):
    repo = get_object_or_404(Repository, pk=pk)
    if request.method == 'POST':
        repo.delete()
        messages.success(request, 'Repository deleted.')
        return redirect('repo_list')
    return render(request, 'core/confirm_delete.html', {'repo': repo})


# ---------------------------------------------------------------------------
# Analytics dashboard - pandas aggregations + Chart.js
# ---------------------------------------------------------------------------
def analytics(request):
    qs = Repository.objects.values(
        'repo_name', 'stars', 'language__name', 'owner__username'
    )
    df = pd.DataFrame(list(qs))

    # Fallback for empty DB
    if df.empty:
        return render(request, 'core/analytics.html', {
            'summary': {},
            'top_repos_json': json.dumps({'labels': [], 'values': []}),
            'language_json': json.dumps({'labels': [], 'values': []}),
            'empty': True,
        })

    # --- Aggregation 1: top 10 repos by stars (bar chart) ---
    top_repos = df.nlargest(10, 'stars')
    top_repos_data = {
        'labels': [
            f"{row['owner__username']}/{row['repo_name']}"
            for _, row in top_repos.iterrows()
        ],
        'values': top_repos['stars'].tolist(),
    }

    # --- Aggregation 2: repos per language (doughnut chart) ---
    lang_counts = (
        df.dropna(subset=['language__name'])
          .groupby('language__name')
          .size()
          .sort_values(ascending=False)
          .head(8)
    )
    language_data = {
        'labels': lang_counts.index.tolist(),
        'values': lang_counts.values.tolist(),
    }

    # --- Aggregation 3: summary stats (table) ---
    stars_desc = df['stars'].describe()
    summary = {
        'Stars (All)': {
            'count': stars_desc['count'],
            'mean': stars_desc['mean'],
            'min': stars_desc['min'],
            'max': stars_desc['max'],
        },
    }
    # Also aggregate avg stars by language
    if not lang_counts.empty:
        avg_by_lang = (
            df.dropna(subset=['language__name'])
              .groupby('language__name')['stars']
              .agg(['count', 'mean', 'min', 'max'])
        )
        for lang, row in avg_by_lang.iterrows():
            summary[f'Stars ({lang})'] = {
                'count': row['count'],
                'mean': row['mean'],
                'min': row['min'],
                'max': row['max'],
            }

    return render(request, 'core/analytics.html', {
        'summary': summary,
        'top_repos_json': json.dumps(top_repos_data),
        'language_json': json.dumps(language_data),
        'empty': False,
    })