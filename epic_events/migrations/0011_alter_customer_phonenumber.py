# Generated by Django 4.1 on 2022-09-19 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epic_events', '0010_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
