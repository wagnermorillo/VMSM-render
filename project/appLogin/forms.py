from django import forms
from .models import Client
from .jsonatrib import clientsAtributes
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
