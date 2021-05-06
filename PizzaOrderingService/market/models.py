from django.db import models


class PizzaFlavor(models.Model):
    val = models.CharField(verbose_name='Flavor', max_length=64, null=False, editable=True)

    def __str__(self):
        return self.val


class Size(models.Model):
    val = models.CharField(verbose_name='Size', max_length=64, null=False, editable=True)

    def __str__(self):
        return self.val


class Pizza(models.Model):
    flavor = models.ForeignKey('PizzaFlavor', null=False, on_delete=models.CASCADE)
    size = models.ForeignKey('Size', null=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('flavor', 'size',)

    def __str__(self):
        return f'{self.size} {self.flavor}'
