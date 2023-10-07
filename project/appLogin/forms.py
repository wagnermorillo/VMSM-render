from dataclasses import field
from typing import Any
from django import forms
from .models import Client, Product, Store
from .jsonatrib import clientsAtributes, productsAtributes, storeAtributes
# forms personalize

# forms to create a Client
class createClient(forms.ModelForm):

    class Meta:
        model = Client
        fields = list(clientsAtributes)
        widgets = {
            "birthdate" : forms.DateInput(attrs={"type" : "date"}),
            "phone" : forms.TextInput(attrs={"data-mask" : "000-000-0000"}),
            "cedula" : forms.TextInput(attrs={"data-mask" : "000-0000000-0"}),
        }

# forms to create a product
class createProduct(forms.ModelForm):

    class Meta:
        model = Product
        fields = list(productsAtributes)

# forms to create a store
class createStore(forms.ModelForm):

    class Meta:
        model = Store
        fields = list(storeAtributes) 