from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

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
def trying(request : HttpRequest) -> HttpResponse:
    return HttpResponse(f"username {request.user.username} password {request.user.password} id {request.user.id}")