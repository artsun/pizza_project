from django.db import transaction
from django.core.validators import MinValueValidator
from rest_framework import serializers
from rest_framework.exceptions import ParseError, APIException

from .models import Order, Customer, Product, Status
from market.models import Pizza
from market.serializers import PizzaSerializer


class StatusSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='val')

    class Meta:
        model = Status
        fields = ('status',)

    def update_order_status(self, order):
        status = Status.objects.filter(val=self.validated_data['val'])
        if status:
            order.status = status[0]
            order.save(update_fields=['status'])
        else:
            raise ParseError('Status does not exists')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('name', 'email', 'address')


class ProductSerializer(serializers.ModelSerializer):
    name = PizzaSerializer()
    number = serializers.IntegerField(required=True, validators=[MinValueValidator(1)])

    class Meta:
        model = Product
        fields = ('name', 'number')


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    products = ProductSerializer(many=True, read_only=False, required=True)
    status = serializers.CharField(source='status.val', required=False)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'products', 'status')

    def create(self, validated_data):
        data = validated_data
        name, email, address = data['customer']['name'], data['customer']['email'], data['customer']['address']
        with transaction.atomic():  # if email existed -> update data, else -> new one
            base_status = Status.get_base_status()
            if base_status is None:
                raise APIException('No base status')
            customer, _ = Customer.objects.update_or_create(email=email, defaults={'name': name, 'address': address})
            order = Order.objects.create(customer=customer, status=base_status)

            for prod in validated_data['products']:
                name = Pizza.objects.select_related('flavor', 'size')\
                    .filter(flavor__val=prod['name']['flavor'], size__val=prod['name']['size'])
                if name:  # handle non-existent Pizza
                    Product.objects.create(name=name[0], order=order, number=prod['number'])

            if not order.products.exists():
                raise ParseError('no products left in the Order')
        return order


class CustomerUpdateSerializer(CustomerSerializer):
    name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    address = serializers.CharField(required=False)


class ProductUpdateSerializer(serializers.ModelSerializer):
    name = PizzaSerializer()
    number = serializers.IntegerField(required=True)

    class Meta:
        model = Product
        fields = ('name', 'number')


class OrderUpdateSerializer(serializers.ModelSerializer):
    customer = CustomerUpdateSerializer(required=False)
    products = ProductUpdateSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'products',)

    def update(self, order, validated_data):
        with transaction.atomic():
            if validated_data.get('customer'):
                [setattr(order.customer, field, val) for field, val in validated_data.get('customer').items()]
                order.customer.save(update_fields=validated_data.get('customer').keys())
            for prod in validated_data['products']:
                name = Pizza.objects.select_related('flavor', 'size')\
                    .filter(flavor__val=prod['name']['flavor'], size__val=prod['name']['size'])
                num = prod['number']
                if name:  # handle non-existent Pizza
                    name = name[0]
                    prod = Product.objects.filter(name=name, order=order)  # dict -> query
                    if num == 0:
                        prod.delete()
                    else:  # update only number if exists
                        prod.update(number=num) if prod else Product.objects.create(name=name, order=order, number=num)
            if not order.products.exists():  # in case of deleted all
                raise ParseError('no products left in the Order')
        return order
