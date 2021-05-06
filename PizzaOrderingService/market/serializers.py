from collections import OrderedDict
from rest_framework import serializers

from .models import Pizza


class PizzaSerializer(serializers.ModelSerializer):
    flavor = serializers.CharField(source='flavor.val')
    size = serializers.CharField(source='size.val')

    class Meta:
        model = Pizza
        fields = ('flavor', 'size')

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        return OrderedDict({"flavor": ret["flavor"]["val"], "size": ret["size"]["val"]})
