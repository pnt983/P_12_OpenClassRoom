from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import SignupUserSerializer, CustomerSerializer
from .models import User, Customer


class SignupUserView(ModelViewSet):
    serializer_class = SignupUserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create_user(first_name=request.data['first_name'],
                                   last_name=request.data['last_name'],
                                   username=request.data['username'],
                                   password=request.data['password'],
                                   is_staff=request.data['is_staff'],
                                   role=request.data['role'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerView(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Customer.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def update(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer, id=kwargs['pk'])
        self.check_object_permissions(self.request, customer)
        serializer = self.serializer_class(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer, id=kwargs['pk'])
        self.check_object_permissions(self.request, customer)
        self.perform_destroy(customer)
        message = f'La compagnie " {customer} " a été correctement supprimé.'
        return Response(message, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=kwargs['pk'])
        if customer:
            serializer = self.serializer_class(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)

