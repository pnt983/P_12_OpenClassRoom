# Generated by Django 4.1 on 2022-09-28 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('epic_events', '0012_alter_contract_client_alter_contract_sales_contact_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='phoneNumber',
            new_name='phone_number',
        ),
    ]
