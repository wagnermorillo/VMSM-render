from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Client, Product
from .jsonatrib import clientsDatatable, productsDatatable
from .forms import createClient, createProduct
from asgiref.sync import sync_to_async
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

    # global variable
    productId = request.GET.get("productId")

    # logic to POST with update products
    if request.method == "POST":
        productId = request.GET.get("productId")
        product = Product.objects.get(pk=productId)
        form = createProduct(request.POST, instance=product)
        form.full_clean()
        if form.is_valid():
            form.save()
            return render(request,
                          "appLogin/productsCreate.html", {
                              "form": form,
                              "success": True,
                              "text": "the product has been updated: "
                          })
        else:
            return render(request,
                          "appLogin/productsCreate.html",
                          {"form": form})

    # logic to GET whith ID product
    if productId:
        product = Product.objects.get(pk=productId)
        form = createProduct(instance=product)
        return render(request,
                      "appLogin/productsCreate.html",
                      {"form": form})

    # normal return
    return render(request, "appLogin/products.html")


@login_required
def productsCreate(request: HttpRequest) -> HttpResponse:

    # logic
    if request.method == "POST":
        form = createProduct(request.POST)
        form.full_clean()
        if form.is_valid():
            form.save()
            return render(request,
                          "appLogin/productsCreate.html", {
                              "form": form,
                              "success": True,
                              "text": "the product has been created: "
                          })
        else:
            return render(request,
                          "appLogin/productsCreate.html",
                          {"form": form})

    form = createProduct()
    return render(request, "appLogin/productsCreate.html", {"form" : form})


#########################################################
#               resources that is not views
#########################################################


# Return data of clients
@login_required
def listClients(request: HttpRequest) -> JsonResponse:
    # query params
    DRAW = int(request.GET.get('draw', 0))
    START = int(request.GET.get('start', 0))
    LENGTH = int(request.GET.get('length', 10))
    SEARCH_VALUE = request.GET.get('search', '').strip()
    clients_list = Client.objects.filter(isDeleted=False).order_by("id")
    
    # Apply search filter if search value is provided
    if SEARCH_VALUE:
        clients_list = clients_list.filter(
            Q(names__icontains=SEARCH_VALUE) |
            Q(lastNames__icontains=SEARCH_VALUE) |
            Q(email__icontains=SEARCH_VALUE) |
            Q(adress__icontains=SEARCH_VALUE) |
            Q(phone__icontains=SEARCH_VALUE) |
            Q(cedula__icontains=SEARCH_VALUE)
        )
    
    # Convert to values after filtering
    clients_list = clients_list.values(*clientsDatatable)
    # Use Paginator
    paginator = Paginator(clients_list, LENGTH)
    PAGENUMBER = (START // LENGTH) + 1

    try:
        clients = paginator.page(PAGENUMBER)
    except PageNotAnInteger:
        # If the page is not an integer, displays the first page.
        clients = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, show the last page of results.
        clients = paginator.page(paginator.num_pages)

    return JsonResponse({
        "clients" : list(clients),
        'draw': DRAW,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
    })

# delete client
async def deleteClient(request: HttpRequest, id : int) -> HttpResponse:
    if request.method == "POST":
        try:
            client = await Client.objects.aget(pk=id)
        except Exception as e:
            return HttpResponse(e)
        client.isDeleted = True
        await client.asave()
        return HttpResponse(status=200)
    


# Return data of products
@login_required
def listProducts(request: HttpRequest) -> HttpResponse:
    # query params
    DRAW = int(request.GET.get('draw', 0))
    START = int(request.GET.get('start', 0))
    LENGTH = int(request.GET.get('length', 10))
    SEARCH_VALUE = request.GET.get('search', '').strip()
    products_list = Product.objects.filter(isDeleted=False).order_by("id")
    
    # Apply search filter if search value is provided
    if SEARCH_VALUE:
        products_list = products_list.filter(
            Q(name__icontains=SEARCH_VALUE) |
            Q(descriptions__icontains=SEARCH_VALUE) 
        )
    
    # Convert to values after filtering
    products_list = products_list.values(*productsDatatable)
    # Use Paginator
    paginator = Paginator(products_list, LENGTH)
    PAGENUMBER = (START // LENGTH) + 1

    try:
        products = paginator.page(PAGENUMBER)
    except PageNotAnInteger:
        # If the page is not an integer, displays the first page.
        products = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, show the last page of results.
        products = paginator.page(paginator.num_pages)

    return JsonResponse({
        "products" : list(products),
        'draw': DRAW,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
    })

# delete client
async def deleteProduct(request: HttpRequest, id : int) -> HttpResponse:
    if request.method == "POST":
        try:
            product = await Product.objects.aget(pk=id)
        except Exception as e:
            return HttpResponse(e)
        product.isDeleted = True
        await product.asave()
        return HttpResponse(status=200)