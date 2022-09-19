from rest_framework.serializers import ModelSerializer

from .models import User, Customer, Contract, StatusEvent, Event


class SignupUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'is_staff', 'role']
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

    def create_user(self, first_name, last_name, username, password, is_staff, role):
        return User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                        password=password, is_staff=is_staff, role=role)


class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'company_name', 'email', 'phoneNumber', 'sales_contact']


class ContractSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = ['sales_contact', 'client', 'amount', 'payment_due']


class StatusEventSerializer(ModelSerializer):

    class Meta:
        model = StatusEvent
        fields = ['description']


class EventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = ['client', 'support_contact', 'contract', 'event_status', 'attendees', 'notes', 'event_date']
