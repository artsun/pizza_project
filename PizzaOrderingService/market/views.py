from rest_framework import viewsets

from .serializers import PizzaSerializer
from .models import Pizza


class Menu(viewsets.ModelViewSet):
    queryset = Pizza.objects.all().order_by('flavor')
    serializer_class = PizzaSerializer
    http_method_names = ('get',)
