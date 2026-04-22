from django.shortcuts import render, redirect, get_object_or_404

# Define views

def home(request):
    return render(request, "core/home.html")

def list(request):
    # To be implemented
    return render(request, "core/list.html")

def list_create(request):
    # To be implemented
    return render(request, "core/form.html")

def list_update(request):
    # To be implemented
    return render(request, "core/form.html")

def list_delete(request):
    # To be implemented
    return render(request, "core/confirm_delete.html")

def analytics(request):
    # To be implemented
    return render(request, "core/analytics.html")