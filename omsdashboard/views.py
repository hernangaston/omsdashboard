from django.shortcuts import render

def index(request):
    return render(request, 'index.html', context={'title':'Index'})

def operation(request, numero):
    return render(request, 'index.html', context={'title':'Index', 'numero':numero})