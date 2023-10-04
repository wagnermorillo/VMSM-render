from django import forms
from .models import Client
from .jsonatrib import clientsAtributes
# forms personalize

# forms to create a Client
class createClient(forms.ModelForm):

    class Meta:
        model = Client
        fields = list(clientsAtributes)