from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    role = [('Managements', 'Managements'),
            ('Sales', 'Sales'),
            ('Supports', 'Supports')]

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    username = models.CharField(max_length=60, unique=True)
    password = models.CharField(max_length=250)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=25, choices=role)

    def __str__(self):
        return self.username


class Customer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    company_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=100, unique=True)
    phoneNumber = models.CharField(max_length=10, unique=True, blank=True)
    is_client = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name


class Contract(models.Model):
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_signed = models.BooleanField(default=False)
    amount = models.FloatField()
    payment_due = models.DateField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contrat du client : {self.client}, par le {self.sales_contact}. "


class StatusEvent(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description


class Event(models.Model):
    client = models.ForeignKey(Customer, on_delete=models.CASCADE)
    support_contact = models.ForeignKey(User, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    event_status = models.ForeignKey(StatusEvent, on_delete=models.CASCADE)
    attendees = models.IntegerField(default=0)
    notes = models.TextField(max_length=2500, null=True, blank=True)
    event_date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Event : {self.client}, {self.contract}, {self.support_contact}"




