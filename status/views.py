from django.shortcuts import render

# Create your views here.

def status(request):
    return render(request, 'status/status.html')

def blank(request):
    return render(request, 'status/blank.html')
