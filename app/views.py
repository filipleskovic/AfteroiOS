from multiprocessing import context
from django.shortcuts import render

from app.models import Party

# Create your views here.


def index(request):
    context = {"parties": Party.objects.all()}
    return render(request, "app/index.html", context)
