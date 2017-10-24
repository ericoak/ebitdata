from django.shortcuts import render

# Create your views here.
from .models import Script

def status(request):
    sta = Script.objects.all()
    context = {'scripts': sta}
    return render(request, 'status/status.html', context)

def blank(request):
    return render(request, 'status/blank.html')
