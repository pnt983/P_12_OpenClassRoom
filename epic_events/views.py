from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
import logging
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import SignupUserSerializer, CustomerSerializer, ContractSerializer, EventSerializer
from .models import User, Customer, Contract, Event
from .permissions import HasSignupPermission, HasCustomerPermission, HasContractPermission, HasEventPermission
from .filters import CustomerFilters, ContractFilters, EventFilters

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
file_handler = logging.FileHandler('test.log')
file_handler.setFormatter(logging_format)

logger.addHandler(file_handler)


class SignupUserView(ModelViewSet):
    serializer_class = SignupUserSerializer
    queryset = User.objects.all()
    permission_classes = [HasSignupPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create_user(first_name=request.data['first_name'],
                                   last_name=request.data['last_name'],
                                   username=request.data['username'],
                                   password=request.data['password'],
                                   is_staff=request.data['is_staff'],
                                   role=request.data['role'])
            logger.info(f"Creation d'un nouvel utilisateur ({request.data['first_name']})")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerView(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated, HasCustomerPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerFilters

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Une compagnie a été crée ({request.data['company_name']})")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def update(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer, id=kwargs['pk'])
        logger.debug(f"request_id : {request.user.id}, sale_contact_id : {customer.sales_contact.id}")
        logger.debug(f"request : {request.user}, sale_contact : {customer.sales_contact}")
        self.check_object_permissions(self.request, customer)
        serializer = self.serializer_class(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Les informations de la compagnie {customer.company_name} ont été mis à jour par {request.user}.")
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer, id=kwargs['pk'])
        self.check_object_permissions(self.request, customer)
        self.perform_destroy(customer)
        message = f'La compagnie " {customer} " a été correctement supprimé.'
        logger.info(f"La compagnie {customer.company_name} a été supprimé par {request.user}.")
        return Response(message, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=kwargs['pk'])
        if customer:
            serializer = self.serializer_class(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ContractView(ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated, HasContractPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractFilters

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Le contrat a été crée par {request.user}.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(serializer.errors)
        return Response(status=status.errors)

    def update(self, request, *args, **kwargs):
        try:
            contract = Contract.objects.get(id=kwargs['pk'])
            self.check_object_permissions(self.request, contract)
            serializer = self.serializer_class(contract, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Le contrat a été modifié par {request.user}.")
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            logger.exception(f"Une exception a été levé : {e}")
            return Response("Le contrat a mettre à jour n'existe pas")

    def destroy(self, request, *args, **kwargs):
        contract = get_object_or_404(Contract, id=kwargs['pk'])
        self.check_object_permissions(self.request, contract)
        self.perform_destroy(contract)
        message = f'Le contrat " {contract} " a été supprimé par {request.user}.'
        return Response(message, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        contract = get_object_or_404(Contract, id=kwargs['pk'])
        if contract:
            serializer = self.serializer_class(contract)
            return Response(serializer.data, status=status.HTTP_200_OK)


class EventView(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, HasEventPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilters

    def create(self, request, *args, **kwargs):
        try:
            contract = Contract.objects.get(id=request.data['contract'])
            if contract.is_signed:
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    logger.info(f"L'événement a été crée par {request.user}.")
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors)
            else:
                return Response("Le contrat doit être signé pour pouvoir créer un événement",
                                status=status.HTTP_417_EXPECTATION_FAILED)
        except ObjectDoesNotExist as e:
            logger.exception(f"Une exception a été levé : {e}")
            return Response("Le contrat pour cet événement n'existe pas", status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=kwargs['pk'])
        self.check_object_permissions(self.request, event)
        serializer = self.serializer_class(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"L'événement a été modifié par {request.user}.")
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=kwargs['pk'])
        self.check_object_permissions(self.request, event)
        self.perform_destroy(event)
        message = f"L'evenement' ' {event} ' a été correctement supprimé."
        logger.info(f"L'événement a été supprimé par {request.user}.")
        return Response(message, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=kwargs['pk'])
        if event:
            serializer = self.serializer_class(event)
            return Response(serializer.data, status=status.HTTP_200_OK)


