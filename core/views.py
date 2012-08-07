from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {})

def schedule(request):
    return render(request, 'agenda.html', {})

def sponsors(request):
    return render(request, 'patrocinadores.html', {})
