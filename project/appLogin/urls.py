from django.urls import path
from . import views

# registar las rutas de la app en especifico
urlpatterns = [
    path("", views.index, name="index")
]