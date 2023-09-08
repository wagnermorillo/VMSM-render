from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

# ejemplo de views
def index(request : HttpRequest) -> HttpResponse:
    return HttpResponse("Hola Mundo!, este es el index")