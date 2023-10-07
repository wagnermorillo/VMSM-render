from collections.abc import Iterable
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator
from django.forms import ValidationError

# validates
phoneValidator = RegexValidator(
    regex=r'^\d{10}$',
    message="The phone number must be exactly 10 digits long."
)
cedulaValidator = RegexValidator(
    regex=r'^\d{11}$',
    message="The phone number must be exactly 11 digits long."
)

# Create your models here.
# clients
class Client(models.Model):

    names = models.CharField("Names", max_length=255)
    lastNames = models.CharField("Last names", max_length=255)
    email = models.EmailField(unique=True)
    adress = models.CharField(max_length=255)
    phone = models.CharField(validators=[phoneValidator], max_length=10)
    cedula = models.CharField(validators=[cedulaValidator], max_length=11, unique=True)
    birthdate = models.DateField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False, editable=False)

    def __str__(self) -> str:
        return f"{self.names}, {self.lastNames}, {self.cedula[:3]}-{self.cedula[3:10]}-{self.cedula[10:]}"
    
    class Meta:
        ordering = ["names"]


# Products
class Product(models.Model):

    name = models.CharField(max_length=255, unique=True)
    descriptions = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False, editable=False)

    def __str__(self) -> str:
        return f"{self.name} {self.descriptions}"
    
    class Meta:
        ordering = ["name"]


# store/inventory
class Store(models.Model):

    location = models.CharField(max_length=255)
    name = models.CharField(max_length=255, unique=True)
    height = models.FloatField(validators=[MinValueValidator(0.0)])
    width = models.FloatField(validators=[MinValueValidator(0.0)])
    depth = models.FloatField(validators=[MinValueValidator(0.0)])
    totalSpace = models.FloatField(validators=[MinValueValidator(0)])
    availableSpace = models.FloatField(validators=[MinValueValidator(0)])
    recordQuantity = models.PositiveIntegerField(default=0)
    adress = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False, editable=False)

    def __str__(self) -> str:
        return f"{self.name} {self.location} {self.totalSpace} {self.adress}"
    
    def clean(self) -> None:
        print("ESTA EN CLEAN()")
        actual_value = Store.objects.get(pk=self.pk).totalSpace if self.pk else None

        # to insert or update the attribute totalSpace
        if actual_value and (not self.totalSpace >= actual_value - self.availableSpace):
            print("TOTASPACE NUEVO NO ES UN VALOR CORRECTO")
            raise ValidationError({
                "error" : "invalid value to TotaSpace"
            })
        else:
            print("TODO FUE BIEN")
            super().clean()
    
    class Meta:
        ordering = ["name"]


# record
class Record(models.Model):

    idClient = models.ForeignKey("Client", on_delete=models.PROTECT)
    idStore = models.ForeignKey("Store", on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, through="RecordProduct")
    dateIn = models.DateField(auto_now_add=True)
    dateOut = models.DateField()
    height = models.FloatField(validators=[MinValueValidator(0.0)])
    width = models.FloatField(validators=[MinValueValidator(0.0)])
    depth = models.FloatField(validators=[MinValueValidator(0.0)])
    totalVolume = models.FloatField(validators=[MinValueValidator(0.0)])
    isFragile = models.BooleanField()
    totalWeight = models.FloatField(validators=[MinValueValidator(0.0)])
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False, editable=False)

    def __str__(self) -> str:
        return f"{self.idClient} {self.idStore} {self.isFragile}"
    
    class Meta:
        ordering = ["dateIn"]


# record_product
class RecordProduct(models.Model):
    
    idRecord = models.ForeignKey("Record", on_delete=models.PROTECT)
    idProduct = models.ForeignKey("Product", on_delete=models.PROTECT)
    quantity =  models.PositiveIntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False, editable=False)

    def __str__(self) -> str:
        return f"{self.idRecord} {self.idProduct} {self.quantity}"
    
    class Meta:
        ordering = ["idRecord"]
    

