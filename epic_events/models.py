from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class User(AbstractBaseUser):

    role = [('Managements', 'Managements'),
            ('Sales', 'Sales'),
            ('Supports', 'Supports')]

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    is_staff = models.BooleanField(default=False)
    groups = models.CharField(max_length=25, choices=role)

    def __str__(self):
        return self.username


class Customer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    company_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=100)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")   # A regler
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=10, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name


class Event(models.Model):

    status_choices = [('En cours', 'En cours')]

    client = models.ForeignKey(Customer, on_delete=models.CASCADE)
    support_contact = models.ForeignKey(User, on_delete=models.CASCADE)
    event_status = models.CharField(max_length=25, choices=status_choices)
    attendees = models.IntegerField()
    notes = models.TextField(max_length=2500, null=True)
    event_date = models.DateTimeField()    # Parametre a definir
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Contract(models.Model):
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)




