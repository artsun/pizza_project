from collections import OrderedDict

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Status, Customer, Order
from market.models import PizzaFlavor, Size, Pizza


class ServeProductTests(APITestCase):

    def setUp(self) -> None:
        Status.objects.create(val='New', number=1)
        Status.objects.create(val='In Progress', number=2)
        Status.objects.create(val='In Delivery', number=3)
        Status.objects.create(val='Finished', number=4)
        small = Size.objects.create(val='Small')
        medium = Size.objects.create(val='Medium')
        large = Size.objects.create(val='Large')
        marinara = PizzaFlavor.objects.create(val='Marinara')
        salami = PizzaFlavor.objects.create(val='Salami')

        Pizza.objects.create(flavor=salami,size=large)
        Pizza.objects.create(flavor=marinara, size=small)
        Pizza.objects.create(flavor=marinara, size=medium)

        self.standart_menu = [
            OrderedDict([("flavor", "Marinara"), ("size", "Small")]),
            OrderedDict([("flavor", "Marinara"), ("size", "Medium")]),
            OrderedDict([("flavor", "Salami"), ("size", "Large")])
        ]
        self.create_order_invalid_payload = {
            "products": [
                {
                    "name": {
                        "flavor": "Marinara",
                        "size": "Medium"
                    },
                    "number": 1
                }
            ]
        }
        self.create_order_valid_payload = {
            "customer": {
                "name": "Example",
                "email": "example@example.com",
                "address": "example street"
            },
            "products": [
                {
                    "name": {
                        "flavor": "Marinara",
                        "size": "Medium"
                    },
                    "number": 1
                }
            ]
        }
        self.customer = ["example@example.com"]

    def test_menu(self):
        url = '/api/menu/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data, self.standart_menu)

    def test_create_order(self):
        url = '/api/orders/'
        response = self.client.post(url, self.create_order_invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(url, self.create_order_valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(list(Customer.objects.filter(name="Example").values_list('email', flat=True)), self.customer)
        self.assertEqual(response.data['status'], 'New')
        self.assertEqual(Order.objects.get(id=response.data['id']).products.count(), 1)
        self.assertEqual(Order.objects.get(id=response.data['id']).products.all()[0].name.flavor.val, "Marinara")
