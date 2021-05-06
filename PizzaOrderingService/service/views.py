from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.views import Response, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from .models import Order
from .serializers import OrderSerializer, OrderUpdateSerializer, StatusSerializer


class OrderHandler(viewsets.ViewSet):

    def create(self, request):
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response(data=order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        if pk is None or not pk.isdigit():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        order = get_object_or_404(Order, pk=pk)
        if order.status.number > 2:
            raise PermissionDenied('Cannot be updated after delivery has been started')

        order_serializer = OrderUpdateSerializer(data=request.data, instance=order)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response(data=order_serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data=order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        filters = {k: v for k, v in request.GET.items() if k in {'customer__name', 'status__val'} and v}
        serializer = OrderSerializer(Order.objects.all().filter(**filters), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if pk is None or not pk.isdigit():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        order = get_object_or_404(Order, pk=pk)
        return Response(OrderSerializer(order).data)

    # track or update status
    @action(methods=['get', 'patch'], detail=True, url_path='status')
    def status(self, request, pk=None):
        if pk is None or not pk.isdigit():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        order = get_object_or_404(Order, pk=pk)
        if request.method == 'PATCH':
            status_serial = StatusSerializer(data=request.data)
            if status_serial.is_valid():
                status_serial.update_order_status(order)
            else:
                return Response(status_serial.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(StatusSerializer(instance=order.status).data)

    def destroy(self, request, pk=None):
        if pk is None or not pk.isdigit():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
