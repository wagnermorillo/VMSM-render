from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.urls import reverse
from .models import Client, Product, Store, Record, RecordProduct
from .forms import createClient, createProduct
from django.contrib.auth.models import User
from django.test import TestCase, Client as ClientTest



class ClientModelTest(TestCase):

    def setUp(self):
        # Crear un cliente para usar en las pruebas
        self.client_obj = Client.objects.create(
            names="John",
            lastNames="Doe",
            email="john.doe@example.com",
            adress="123 Main St",
            phone="1234567890",
            cedula="12345678901",
            birthdate="1990-01-01"
        )

    def test_create_client(self):
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(self.client_obj.names, "John")

    def test_phone_validation(self):
        # Probar un número de teléfono válido
        self.client_obj.phone = "1234567890"
        self.client_obj.full_clean()  # No debería lanzar excepción

        # Probar un número de teléfono inválido
        self.client_obj.phone = "12345"
        with self.assertRaises(ValidationError):
            self.client_obj.full_clean()

    def test_cedula_validation(self):
        # Probar una cédula válida
        self.client_obj.cedula = "12345678901"
        self.client_obj.full_clean()  # No debería lanzar excepción

        # Probar una cédula inválida
        self.client_obj.cedula = "12345"
        with self.assertRaises(ValidationError):
            self.client_obj.full_clean()

    def test_unique_fields(self):
        # Probar que el email y la cédula deben ser únicos
        with self.assertRaises(IntegrityError):
            Client.objects.create(
                names="Jane",
                lastNames="Doe",
                email="john.doe@example.com",  # Email duplicado
                adress="456 Elm St",
                phone="0987654321",
                cedula="12345678901",  # Cédula duplicada
                birthdate="1995-01-01"
            )

    def test_string_representation(self):
        self.assertEqual(str(self.client_obj), "John, Doe, 123-4567890-1")


class ProductModelTest(TestCase):

    def setUp(self):
        # Crear un producto para usar en varios tests
        self.product = Product.objects.create(
            name="Test Product",
            descriptions="This is a test product."
        )

    def test_create_product(self):
        """Test para verificar la creación exitosa de un producto."""
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.descriptions, "This is a test product.")
        self.assertFalse(self.product.isDeleted)

    def test_name_uniqueness(self):
        """Test para verificar que no se pueden crear dos productos con el mismo nombre."""
        with self.assertRaises(Exception):  # Esperamos una excepción debido a la unicidad
            Product.objects.create(
                name="Test Product",  # Mismo nombre que el producto creado en setUp
                descriptions="Another description."
            )

    def test_default_isDeleted(self):
        """Test para verificar que el valor por defecto de isDeleted es False."""
        self.assertFalse(self.product.isDeleted)

    def test_str_representation(self):
        """Test para verificar la representación de cadena del modelo."""
        self.assertEqual(str(self.product),
                         "Test Product This is a test product.")


class StoreModelTest(TestCase):

    def setUp(self):
        # Crear una tienda para usar en varios tests
        self.store = Store.objects.create(
            location="Test Location",
            name="Test Store",
            height=10.0,
            width=10.0,
            depth=10.0,
            totalSpace=1000.0,
            availableSpace=500.0,
            adress="123 Test St."
        )

    def test_create_store(self):
        """Test para verificar la creación exitosa de una tienda."""
        self.assertEqual(self.store.name, "Test Store")
        self.assertEqual(self.store.location, "Test Location")
        self.assertEqual(self.store.totalSpace, 1000.0)
        self.assertFalse(self.store.isDeleted)

    def test_name_uniqueness(self):
        """Test para verificar que no se pueden crear dos tiendas con el mismo nombre."""
        with self.assertRaises(Exception):  # Esperamos una excepción debido a la unicidad
            Store.objects.create(
                location="Another Location",
                name="Test Store",  # Mismo nombre que la tienda creada en setUp
                height=5.0,
                width=5.0,
                depth=5.0,
                totalSpace=250.0,
                availableSpace=125.0,
                adress="456 Another St."
            )

    def test_negative_values(self):
        """Test para verificar que no se pueden ingresar valores negativos."""
        negative_store = Store(
            location="Negative Test",
            name="Negative Store",
            height=-10.0,
            width=-10.0,
            depth=-10.0,
            totalSpace=-1000.0,
            availableSpace=-500.0,
            adress="789 Negative St."
        )
        with self.assertRaises(ValidationError):
            negative_store.full_clean()

    def test_str_representation(self):
        """Test para verificar la representación de cadena del modelo."""
        self.assertEqual(
            str(self.store), "Test Store Test Location 1000.0 123 Test St.")

    def test_clean_method(self):
        """Test para verificar la validación del método clean para el campo totalSpace."""
        self.store.totalSpace = 400.0
        with self.assertRaises(ValidationError):
            self.store.clean()


class RecordModelTest(TestCase):

    def setUp(self):
        self.client_obj = Client.objects.create(
            names="Test Client",
            lastNames="Last Name",
            email="test@email.com",
            adress="Test Address",
            phone="1234567890",
            cedula="12345678901",
            birthdate="1990-01-01"
        )
        self.store_obj = Store.objects.create(
            location="Test Location",
            name="Test Store",
            height=10.0,
            width=10.0,
            depth=10.0,
            totalSpace=1000.0,
            availableSpace=900.0,
            recordQuantity=1,
            adress="Test Address"
        )
        self.product_obj = Product.objects.create(
            name="Test Product",
            descriptions="Test Description"
        )

    def test_valid_record_creation(self):
        record = Record.objects.create(
            idClient=self.client_obj,
            idStore=self.store_obj,
            dateIn="2022-01-01",
            dateOut="2022-01-02",
            height=5.0,
            width=5.0,
            depth=5.0,
            totalVolume=125.0,
            isFragile=True,
            totalWeight=10.0
        )
        record_product_relation = RecordProduct.objects.create(
            idRecord=record,
            idProduct=self.product_obj,
            quantity= 10
        )
        record.products.add(self.product_obj)
        self.assertEqual(record.idClient, self.client_obj)
        self.assertEqual(record.idStore, self.store_obj)
        self.assertTrue(self.product_obj in record.products.all())

    def test_invalid_date(self):
        with self.assertRaises(ValidationError):
            record = Record(
                idClient=self.client_obj,
                idStore=self.store_obj,
                dateIn="2022-01-03",
                dateOut="2022-01-02",
                height=5.0,
                width=5.0,
                depth=5.0,
                totalVolume=125.0,
                isFragile=True,
                totalWeight=10.0
            )
            record.clean()

    def test_negative_height(self):
        negative_record = Record.objects.create(
            idClient=self.client_obj,
            idStore=self.store_obj,
            dateIn="2022-01-01",
            dateOut="2022-01-02",
            height=-5.0,
            width=5.0,
            depth=5.0,
            totalVolume=125.0,
            isFragile=True,
            totalWeight=10.0
        )
        with self.assertRaises(ValidationError):
            negative_record.full_clean()


class RecordProductModelTest(TestCase):

    def setUp(self):
        # Crear instancias de los modelos necesarios para las relaciones ForeignKey
        self.client_obj = Client.objects.create(
            names="John",
            lastNames="Doe",
            email="john.doe@example.com",
            adress="123 Main St",
            phone="1234567890",
            cedula="12345678901",
            birthdate="1990-01-01"
        )
        self.store_obj = Store.objects.create(
            location="Location1",
            name="Store1",
            height=10.0,
            width=10.0,
            depth=10.0,
            totalSpace=1000.0,
            availableSpace=900.0,
            recordQuantity=1,
            adress="123 Store St"
        )
        self.product_obj = Product.objects.create(
            name="Product1",
            descriptions="Description1"
        )
        self.record_obj = Record.objects.create(
            idClient=self.client_obj,
            idStore=self.store_obj,
            dateIn="2023-01-01",
            dateOut="2023-01-02",
            height=5.0,
            width=5.0,
            depth=5.0,
            totalVolume=125.0,
            isFragile=True,
            totalWeight=50.0
        )

    def test_create_record_product(self):
        # Test para crear un RecordProduct
        record_product = RecordProduct.objects.create(
            idRecord=self.record_obj,
            idProduct=self.product_obj,
            quantity=5
        )
        self.assertEqual(record_product.quantity, 5)

    def test_unique_constraint(self):
        # Test para la restricción de integridad única
        RecordProduct.objects.create(
            idRecord=self.record_obj,
            idProduct=self.product_obj,
            quantity=5
        )
        with self.assertRaises(Exception):
            RecordProduct.objects.create(
                idRecord=self.record_obj,
                idProduct=self.product_obj,
                quantity=10
            )

    def test_logical_delete(self):
        # Test para la eliminación lógica
        record_product = RecordProduct.objects.create(
            idRecord=self.record_obj,
            idProduct=self.product_obj,
            quantity=5
        )
        record_product.isDeleted = True
        record_product.save()
        self.assertTrue(record_product.isDeleted)



class UserModelTest(TestCase):

    def setUp(self):
        # Crear un usuario para usar en los tests
        self.user = User.objects.create_user(
            username="johndoe",
            email="johndoe@example.com",
            password="testpassword123"
        )

    def test_user_creation(self):
        # Test para verificar la creación de un usuario
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, "johndoe")
        self.assertEqual(self.user.email, "johndoe@example.com")

    def test_user_str_representation(self):
        # Test para verificar la representación en cadena del usuario
        self.assertEqual(str(self.user), "johndoe")

    def test_user_password(self):
        # Test para verificar que el password se ha encriptado
        self.assertNotEqual(self.user.password, "testpassword123")
        self.assertTrue(self.user.check_password("testpassword123"))

    def test_user_is_active_by_default(self):
        # Test para verificar que el usuario está activo por defecto
        self.assertTrue(self.user.is_active)


class CreateClientFormTest(TestCase):

    def test_valid_form(self):
        data = {
            'names': 'John',
            'lastNames': 'Doe',
            'email': 'john.doe@example.com',
            'adress': '123 Main St',
            'phone': '1234567890',
            'cedula': '12345678901',
            'birthdate': '1990-01-01',
        }
        form = createClient(data)
        self.assertTrue(form.is_valid())

    def test_missing_field(self):
        data = {
            'names': 'John',
            'lastNames': 'Doe',
            'email': 'john.doe@example.com',
            'adress': '123 Main St',
            'phone': '123-456-7890',
            'birthdate': '1990-01-01',
        }
        form = createClient(data)
        self.assertFalse(form.is_valid())

    def test_phone_format(self):
        data = {
            'names': 'John',
            'lastNames': 'Doe',
            'email': 'john.doe@example.com',
            'adress': '123 Main St',
            'phone': '1234567890',  # Incorrect format
            'cedula': '123-4567890-1',
            'birthdate': '1990-01-01',
        }
        form = createClient(data)
        self.assertFalse(form.is_valid())

    def test_cedula_format(self):
        data = {
            'names': 'John',
            'lastNames': 'Doe',
            'email': 'john.doe@example.com',
            'adress': '123 Main St',
            'phone': '123-456-7890',
            'cedula': '12345678901',  # Incorrect format
            'birthdate': '1990-01-01',
        }
        form = createClient(data)
        self.assertFalse(form.is_valid())


class CreateProductFormTest(TestCase):

    def test_valid_form(self):
        data = {
            'name': 'Sample Product',
            'descriptions': 'This is a sample product description.',
        }
        form = createProduct(data)
        self.assertTrue(form.is_valid())

    def test_missing_field(self):
        data = {
            'name': 'Sample Product',
        }
        form = createProduct(data)
        self.assertFalse(form.is_valid())

    def test_duplicate_product_name(self):
        Product.objects.create(name='Sample Product', descriptions='Description')
        data = {
            'name': 'Sample Product',
            'descriptions': 'Another description for the same product name.',
        }
        form = createProduct(data)
        self.assertFalse(form.is_valid())


class ListClientsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.test_user = User.objects.create_user(username='testuser', password='testpass')

        # Create some clients
        for i in range(10):
            Client.objects.create(
                names=f"Name {i}",
                lastNames=f"LastName {i}",
                email=f"test{i}@example.com",
                adress=f"Address {i}",
                phone=f"123456789{i}",
                cedula=f"1234567890{i}",
                birthdate="2000-01-01"
            )

    def setUp(self):
        self.client = ClientTest()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('listClients'))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

    def test_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('listClients'), {'draw': 1, 'start': 0, 'length': 10})
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('clients', json_response)
        self.assertIn('draw', json_response)
        self.assertIn('recordsTotal', json_response)
        self.assertIn('recordsFiltered', json_response)

    def test_search_filter(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('listClients'), {'draw': 1, 'start': 0, 'length': 10, 'search': 'Name 5'})
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(len(json_response['clients']), 1)
        self.assertEqual(json_response['clients'][0]['names'], 'Name 5')


class StoresViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.test_user = User.objects.create_user(username='testuser', password='testpass')

        # Create some stores
        cls.store = Store.objects.create(
            location="Test Location",
            name="Test Store",
            height=10.0,
            width=10.0,
            depth=10.0,
            totalSpace=1000.0,
            availableSpace=1000.0,
            recordQuantity=0,
            adress="Test Address"
        )

    def setUp(self):
        self.client = ClientTest()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('stores'))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

    def test_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('stores'))
        self.assertEqual(response.status_code, 200)

    def test_update_store_with_post_request(self):
        self.client.login(username='testuser', password='testpass')
        form_data = {
            'location': 'Updated Location',
            'name': 'Updated Store',
            'height': 20.0,
            'width': 20.0,
            'depth': 20.0,
            'adress': 'Updated Address'
        }
        response = self.client.post(reverse('stores') + f'?storeId={self.store.id}', form_data)
        self.assertEqual(response.status_code, 200)
        self.store.refresh_from_db()
        self.assertEqual(self.store.location, 'Updated Location')
        self.assertEqual(self.store.name, 'Updated Store')