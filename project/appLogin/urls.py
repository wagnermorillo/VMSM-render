from django.urls import include, path
from . import views

# registar las rutas de la app en especifico
urlpatterns = [
    path('', views.redic, name="redirect"),
    path("home/", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("dashboard/", views.trying, name="dashboard"),
]