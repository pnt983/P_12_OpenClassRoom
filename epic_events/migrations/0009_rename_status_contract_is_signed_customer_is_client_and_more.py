# Generated by Django 4.1 on 2022-09-07 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epic_events', '0008_statusevent_event_contract_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='status',
            new_name='is_signed',
        ),
        migrations.AddField(
            model_name='customer',
            name='is_client',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contract',
            name='payment_due',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='attendees',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='event',
            name='notes',
            field=models.TextField(blank=True, max_length=2500, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]
