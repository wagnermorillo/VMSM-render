from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Client
from .jsonatrib import clientsDatatable
from .forms import createClient
# Create your views here


# ejemplo de views
# views para redireccionar a home
def redic(request : HttpRequest) -> HttpResponse:
    return redirect("home/")

# views home
def index(request : HttpRequest) -> HttpResponse:
    return render(request, 'appLogin/index.html')

#views about
def about(request : HttpRequest) -> HttpResponse:
    return render(request, 'appLogin/about.html')

#views contact
def contact(request : HttpRequest) -> HttpResponse:
    return render(request, 'appLogin/contact.html')

# views dashboard user already logged
@login_required
def home(request : HttpRequest) -> HttpResponse:
    return render(request, "appLogin/main.html")

# views main customers/clients
@login_required
def customers(request : HttpRequest) -> HttpResponse:
    # logic
    form = createClient()
    return render(request, 
                  "appLogin/customers.html",
                  {"form" : form})


# Return data of clients
@login_required
def listClients(request : HttpRequest) -> HttpResponse:
    clients = list(Client.objects.filter(isDeleted=False).values(*clientsDatatable))
    return JsonResponse({
        "clients" : clients
    })

