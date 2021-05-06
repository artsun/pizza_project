from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):
    name = models.ForeignKey('market.Pizza', null=False, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', null=False, on_delete=models.CASCADE, related_name='products')
    number = models.PositiveSmallIntegerField(null=False, editable=True, default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('id', 'name', 'order')

    def __str__(self):
        return f'{self.name} <- {self.order}'


class Status(models.Model):
    val = models.CharField(verbose_name='Status', max_length=64, null=False, editable=True)
    number = models.PositiveSmallIntegerField(null=False, editable=True, unique=True)

    class Meta:
        verbose_name_plural = "Statuses"

    def __str__(self):
        return self.val

    @staticmethod
    def get_base_status():
        try:
            return Status.objects.get(number=1)
        except Status.DoesNotExist:
            return None


class Customer(models.Model):
    name = models.CharField(max_length=64, null=False, editable=True)
    email = models.EmailField(max_length=64, null=False, editable=True)
    address = models.CharField(max_length=256, null=False, editable=True)

    def __str__(self):
        return self.email


class Order(models.Model):
    customer = models.ForeignKey('Customer', null=False, on_delete=models.CASCADE, related_name='orders')
    status = models.ForeignKey('Status', null=False, on_delete=models.CASCADE, related_name='orders')
    created = models.DateTimeField(auto_now_add=True, null=False)
    status_updated = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return f'{self.customer} - {self.created.strftime("%d %m %Y %H:%M:%S")}'
