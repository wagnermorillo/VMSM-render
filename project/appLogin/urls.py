from django.urls import include, path
from . import views

# registar las rutas de la app en especifico
urlpatterns = [

    # landing page
    path('', views.redic, name="redirect"),
    path("home/", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    
    # resources
    path("resources/listClients/", views.listClients, name="listClients"),
    path("resources/listClients/<int:id>/", views.getClient, name="getClient"),
    path("resources/deleteClient/<int:id>/", views.deleteClient, name="deleteClient"),
    path("resources/listProducts/", views.listProducts, name="listProducts"),
    path("resources/listProducts/<int:id>/", views.getProducts, name="getProducts"),
    path("resources/deleteProduct/<int:id>/", views.deleteProduct, name="deleteProduct"),
    path("resources/listStores/", views.listStores, name="listStores"),
    path("resources/listStores/<int:id>/", views.getStore, name="getStore"),
    path("resources/deleteStore/<int:id>/", views.deleteStore, name="deleteStore"),
    path("resources/listRecords/", views.listRecords, name="listRecords"),

    # main
    path("main/home/", views.home, name="mainHome"),
    path("main/customers/", views.customers, name="customers"),
    path("main/customers/create/", views.customersCreate, name="customersCreate"),
    path("main/products/", views.products, name="products"),
    path("main/products/create/", views.productsCreate, name="productsCreate"),
    path("main/stores/", views.stores, name="stores"),
    path("main/stores/create/", views.storesCreate, name="storesCreate"),
    path("main/registers/", views.registers, name="registers"), # nuevo registro/switch

    #TESTING
    path("main/testing/", views.testing, name="testing"), # nuevo registro/switch
    path('get_store_dimensions/<int:store_id>/', views.get_store_dimensions, name='get_store_dimensions'),
    path('get_full_spaces/<int:store_id>/', views.get_full_spaces, name='get_full_spaces'),
    path("api/get_client_fullName/", views.get_client_fullName, name='get_client_fullName'),
    path("api/obtener_almacenes/", views.obtener_almacenes, name="obtener_almacenes"),
    path('get_records_in_store/<int:store_id>/', views.get_records_in_store, name='get_records_in_store'),
]