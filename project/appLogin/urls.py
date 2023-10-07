from django.urls import include, path
from . import views

# registar las rutas de la app en especifico
urlpatterns = [
    path('', views.redic, name="redirect"),
    path("home/", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("main/home/", views.home, name="mainHome"),
    path("resources/listClients/", views.listClients, name="listClients"),
    path("resources/deleteClient/<int:id>/", views.deleteClient, name="deleteClient"),
    path("resources/listProducts/", views.listProducts, name="listProducts"),
    path("resources/deleteProduct/<int:id>/", views.deleteProduct, name="deleteProduct"),
    path("main/customers/", views.customers, name="customers"),
    path("main/customers/create/", views.customersCreate, name="customersCreate"),
    path("main/products/", views.products, name="products"),
    path("main/products/create/", views.productsCreate, name="productsCreate"),
]