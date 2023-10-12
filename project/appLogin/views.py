from django.http import JsonResponse
from .models import Store, Client, Record
from django.shortcuts import render
from django.forms import ValidationError
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Value, CharField
from django.db.models.functions import Concat
from django.db import transaction, DatabaseError
from .models import Client, Product, Record, Store, RecordProduct
from .jsonatrib import clientsDatatable, productsDatatable, storesDatatable, recordsDatatable, clientsAtributes
from .forms import createClient, createProduct, createStore
from asgiref.sync import sync_to_async
# Create your views here
# ejemplo de views

#########################################################
#               views of landing page
#########################################################

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


#########################################################
#               views of register/record
#########################################################


# table format to READ record


def registers(request: HttpRequest) -> HttpResponse:

    # normal render
    return render(request,
                  "appLogin/record.html")


#########################################################
#               views of client
#########################################################


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
    return render(request, "appLogin/customersCreate.html", {"form": form})


#########################################################
#               views of product
#########################################################


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
    return render(request, "appLogin/productsCreate.html", {"form": form})


#########################################################
#               views of store
#########################################################

@sync_to_async
@login_required
def stores(request: HttpRequest) -> HttpResponse:

    # global variable
    storeId = request.GET.get("storeId")
    print(storeId)

    # logic to POST with update products
    if request.method == "POST":
        storeId = request.GET.get("storeId")
        store = Store.objects.get(pk=storeId)
        form = createStore(request.POST, instance=store)
        form.full_clean()
        if form.is_valid():

            # refill atributes that there are not in form
            form.instance.totalSpace = form.cleaned_data["height"] * \
                form.cleaned_data["width"] * form.cleaned_data["depth"]
            form.instance.availableSpace = form.instance.totalSpace

            # can ocurr a error in save
            try:
                form.save()
                return render(request,
                              "appLogin/storesCreate.html", {
                                  "form": form,
                                  "success": True,
                                  "text": "the store has been updates: "
                              })

            # if ocurr a error
            except ValidationError as e:
                print(e)
                return render(request,
                              "appLogin/storesCreate.html", {
                                  "form": form,
                                  "ERROR": ""
                              })
        else:
            return render(request,
                          "appLogin/storesCreate.html",
                          {"form": form})

    # logic to Get store form
    if storeId:
        store = Store.objects.get(pk=storeId)
        form = createStore(instance=store)
        return render(request,
                      "appLogin/storesCreate.html",
                      {"form": form})

    # normal return
    return render(request, "appLogin/stores.html")


@login_required
def storesCreate(request: HttpRequest) -> HttpResponse:

    # logic to create
    if request.method == "POST":
        form = createStore(request.POST)
        form.full_clean()
        if form.is_valid():

            # refill atributes that there are not in form
            form.instance.totalSpace = form.cleaned_data["height"] * \
                form.cleaned_data["width"] * form.cleaned_data["depth"]
            form.instance.availableSpace = form.instance.totalSpace
            form.save()

            # return the store created
            return render(request,
                          "appLogin/storesCreate.html", {
                              "form": form,
                              "success": True,
                              "text": "the store has been created: "
                          })

        # form is not valid
        else:
            return render(request,
                          "appLogin/storesCreate.html",
                          {"form": form})

    form = createStore()
    return render(request, "appLogin/storesCreate.html", {"form": form})


#########################################################
#               resources that is not views
#########################################################


# Return data of clients
@sync_to_async
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
        "clients": list(clients),
        'draw': DRAW,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
    })

# delete client


@sync_to_async
@login_required
def deleteClient(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "POST":
        try:
            with transaction.atomic():
                client = Client.objects.get(pk=id)
                client.record_set.update(isDeleted=True)
                client.isDeleted = True
                client.save()
                # all was OK
                return HttpResponse(status=200)
        except DatabaseError as e:
            return Http404(e)


# get client by id only one
async def getClient(request: HttpRequest, id: int) -> HttpResponse:

    if request.method == "GET":
        try:
            client = await Client.objects.aget(pk=id)
            # convert to a dict
            data = {
                "names": client.names,
                "lastNames": client.lastNames,
                "email": client.email,
                "adress": client.adress,
                "phone": client.phone,
                "cedula": client.cedula,
                "birthdate": client.birthdate,
            }
            return JsonResponse({
                "client": data
            })
        except Exception as e:
            return Http404("client not found")


# Return data of products
@sync_to_async
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
        "products": list(products),
        'draw': DRAW,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
    })


# delete product
async def deleteProduct(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "POST":
        try:
            product = await Product.objects.aget(pk=id)
            product.isDeleted = True
            await product.asave()
            return HttpResponse(status=200)
        except Exception as e:
            return Http404(e)


# get all product relation with a record
def getProducts(request: HttpRequest, id: int) -> HttpResponse:

    if request.method == "GET":
        # Get all products and quantities related to that record
        productRelated = RecordProduct.objects.filter(
            isDeleted=False,
            idRecord=id
        ).values("idProduct__name", "quantity")

        # return all products related
        return JsonResponse({
            "products": list(productRelated)
        })


# return data of store
@sync_to_async
@login_required
def listStores(request: HttpRequest) -> HttpResponse:
    # query params
    DRAW = int(request.GET.get('draw', 0))
    START = int(request.GET.get('start', 0))
    LENGTH = int(request.GET.get('length', 10))
    SEARCH_VALUE = request.GET.get('search', '').strip()
    stores_list = Store.objects.filter(isDeleted=False).order_by("id")

    # Apply search filter if search value is provided
    if SEARCH_VALUE:
        stores_list = stores_list.filter(
            Q(name__icontains=SEARCH_VALUE) |
            Q(height__icontains=SEARCH_VALUE) |
            Q(width__icontains=SEARCH_VALUE) |
            Q(depth__icontains=SEARCH_VALUE) |
            Q(location__icontains=SEARCH_VALUE) |
            Q(totalSpace__icontains=SEARCH_VALUE) |
            Q(availableSpace__icontains=SEARCH_VALUE) |
            Q(recordQuantity__icontains=SEARCH_VALUE) |
            Q(adress__icontains=SEARCH_VALUE)
        )

    # Convert to values after filtering
    stores_list = stores_list.values(*storesDatatable)
    # Use Paginator
    paginator = Paginator(stores_list, LENGTH)
    PAGENUMBER = (START // LENGTH) + 1

    try:
        stores = paginator.page(PAGENUMBER)
    except PageNotAnInteger:
        # If the page is not an integer, displays the first page.
        stores = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, show the last page of results.
        stores = paginator.page(paginator.num_pages)

    return JsonResponse({
        "stores": list(stores),
        'draw': DRAW,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
    })


# delete a store
@sync_to_async
@login_required
def deleteStore(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "POST":
        try:
            with transaction.atomic():
                store = Store.objects.get(pk=id)
                store.record_set.update(isDeleted=True)
                store.isDeleted = True
                store.save()
            return HttpResponse(status=200)
        except Exception as e:
            return Http404(e)


# get store by id only one
async def getStore(request: HttpRequest, id: int) -> HttpResponse:

    if request.method == "GET":
        try:
            store = await Store.objects.aget(pk=id)
            # convert to a dict
            data = {
                "location": store.location,
                "name": store.name,
                "height": store.height,
                "width": store.width,
                "depth": store.depth,
                "totalSpace": store.totalSpace,
                "availableSpace": store.availableSpace,
                "recordQuantity": store.recordQuantity,
                "adress": store.adress,
            }
            return JsonResponse({
                "store": data
            })
        except Exception as e:
            return Http404("client not found")


# return data of store
@sync_to_async
@login_required
def listRecords(request: HttpRequest) -> HttpResponse:

    # query params
    DRAW = int(request.GET.get('draw', 0))
    START = int(request.GET.get('start', 0))
    LENGTH = int(request.GET.get('length', 10))
    SEARCH_VALUE = request.GET.get('search', '').strip()

    record_list = Record.objects.filter(isDeleted=False).annotate(clientFullName=Concat(
        F("idClient__names"),
        Value(" "),
        F("idClient__lastNames"),
        output_field=CharField(),),
        storeName=F("idStore__name")).order_by("id")

    # apply seach filter if search value is provided
    if SEARCH_VALUE:
        record_list = record_list.filter(
            Q(clientFullName__icontains=SEARCH_VALUE) |
            Q(storeName__icontains=SEARCH_VALUE) |
            Q(height__icontains=SEARCH_VALUE) |
            Q(width__icontains=SEARCH_VALUE) |
            Q(depth__icontains=SEARCH_VALUE) |
            Q(dateIn__icontains=SEARCH_VALUE) |
            Q(dateOut__icontains=SEARCH_VALUE) |
            Q(totalVolume__icontains=SEARCH_VALUE) |
            Q(totalWeight__icontains=SEARCH_VALUE)
        )

    # convert to values after filtering
    record_list = record_list.values(
        "clientFullName", "storeName", *recordsDatatable)

    # Use paginator
    paginator = Paginator(record_list, LENGTH)
    PAGENUMBER = (START // LENGTH) + 1

    try:
        record = paginator.page(PAGENUMBER)
    except PageNotAnInteger:
        # If the page is not an integer, displays the first page.
        record = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, show the last page of results.
        record = paginator.page(paginator.num_pages)
    return JsonResponse({
        "records": list(record),
        'draw': DRAW,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
    })


#########################################################
#               views of TESTING
#########################################################
# views.py


@login_required
def testing(request: HttpRequest) -> HttpResponse:
    return render(request, "appLogin/almacen_matriz.html")


def almacen_matriz(request):
    # Obtén la lista de almacenes
    stores = Store.objects.all()

    context = {
        'stores': stores,  # Pasa la lista de almacenes al contexto
    }

    return render(request, 'almacen_matriz.html', context)


def get_store_dimensions(request, store_id):
    try:
        store = Store.objects.get(id=store_id)
        dimensions = {
            'height': store.height,
            'width': store.width,
        }
        return JsonResponse(dimensions)
    except Store.DoesNotExist:
        return JsonResponse({'error': 'Almacén no encontrado'}, status=404)
   
def get_full_spaces(request, store_id):
    try:
        record = Record.objects.get(idStore=store_id)
        fullName = {
            'idSpace': record.idSpace,
        }
        return JsonResponse(fullName)
    except Store.DoesNotExist:
        return JsonResponse({'error': 'Almacén no encontrado'}, status=404)    


def obtener_almacenes(request):
    almacenes = Store.objects.filter(isDeleted=False).values("id", "name")
    return JsonResponse({"almacenes": list(almacenes)})

def get_client_fullName(request):
    clients = Client.objects.filter(isDeleted=False).values("id", "names", "lastNames")
    return JsonResponse({"client": list(clients)})

def get_records_in_store(request, store_id):
    try:
        # Recupera los registros del almacén especificado por store_id
        records = Record.objects.filter(idStore=store_id, isDeleted=False).values("id", "idClient__names", "idClient__lastNames", "dateIn", "dateOut", "width", "height", "widthPosition", "heightPosition")

        return JsonResponse({"records": list(records)})
    except Exception as e:
        return JsonResponse({'error': 'Error al obtener los registros del almacén'}, status=500)

