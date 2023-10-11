# module to write the attribute that i want to response of my models

# Client attributes
clientsAtributes = (
    "names",
    "lastNames",
    "email",
    "adress",
    "phone",
    "cedula",
    "birthdate",
)

# Client atrributes datatable
clientsDatatable = (
    "id",
    "names",
    "lastNames",
    "email",
    "phone",
    "cedula",
    "birthdate",
)

# Product attributes datatable
productsDatatable = {
    "id",
    "name",
    "descriptions",
}

# Product attributes
productsAtributes = (
    "name",
    "descriptions",
)

# Store atrributes datatable
storesDatatable = {
    "id",
    "location",
    "name",
    "height",
    "width",
    "depth",
    "totalSpace",
    "availableSpace",
    "recordQuantity",
    "adress",
}

# Store attributes
storeAtributes = (
    "location",
    "name",
    "height",
    "width",
    "depth",
    "adress",
)

# Record atrributes datatable
recordsDatatable ={
    "id",
    "idClient",
    "idStore",
    "dateIn",
    "dateOut",
    "height",
    "width",
    "depth",
    "totalVolume",
    "isFragile",
    "totalWeight",
}