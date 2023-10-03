from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views he

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
def main(request : HttpRequest) -> HttpResponse:
    return render(request, 'appLogin/main.html')