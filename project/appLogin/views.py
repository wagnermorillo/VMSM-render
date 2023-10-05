from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Client
from .jsonatrib import clientsDatatable
from .forms import createClient
# Create your views here


# ejemplo de views
# views para redireccionar a home
def redic(request: HttpRequest) -> HttpResponse:
    return redirect("home/")

# views home
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'appLogin/index.html')

# views about
def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'appLogin/about.html')

# views contact
def contact(request: HttpRequest) -> HttpResponse:
    return render(request, 'appLogin/contact.html')

# views dashboard user already logged
@login_required
def home(request: HttpRequest) -> HttpResponse:
    return render(request, "appLogin/main.html")

# views to see the datatable client
@login_required
def customers(request: HttpRequest) -> HttpResponse:

    # global variable
    clientId = request.GET.get("clientId")

    # logic to POST with update client
    if request.method == "POST":
        clientId = request.GET.get("clientId")
        client = Client.objects.get(pk=clientId)
        form = createClient(request.POST, instance=client)
        form.full_clean()
        if form.is_valid():
            form.save()
            return render(request,
                          "appLogin/customersCreate.html", {
                              "form": form,
                              "success": True,
                              "text": "the customer has been updated: "
                          })
        else:
            return render(request,
                          "appLogin/customersCreate.html",
                          {"form": form})

    # logic to GET whith ID client
    if clientId:
        client = Client.objects.get(pk=clientId)
        form = createClient(instance=client)
        return render(request,
                      "appLogin/customersCreate.html",
                      {"form": form})

    # normal return
    return render(request, "appLogin/customers.html")

# views to create a client
@login_required
def customersCreate(request: HttpRequest) -> HttpResponse:

    # logic
    if request.method == "POST":
        form = createClient(request.POST)
        form.full_clean()
        if form.is_valid():
            form.save()
            return render(request,
                          "appLogin/customersCreate.html", {
                              "form": form,
                              "success": True,
                              "text": "the customer has been created: "
                          })
        else:
            return render(request,
                          "appLogin/customersCreate.html",
                          {"form": form})

    form = createClient()
    return render(request, "appLogin/customersCreate.html", {"form" : form})

# views to product
@login_required
def products(request: HttpRequest) -> HttpResponse:
    return render(request, "appLogin/products.html")


#########################################################
#               resources that is not views
#########################################################
# Return data of clients
@login_required
def listClients(request: HttpRequest) -> HttpResponse:
    clients = list(Client.objects.filter(isDeleted=False).values(*clientsDatatable).order_by("id"))
    return JsonResponse({
        "clients": clients
    })

# delete client
@login_required
def deleteClient(request: HttpRequest, id : int) -> HttpResponse:
    if request.method == "POST":
        try:
            client = Client.objects.get(pk=id)
        except Exception as e:
            HttpResponse(e)
        client.isDeleted = True
        client.save()
        return HttpResponse(status=200)