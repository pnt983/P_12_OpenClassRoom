# Generated by Django 4.1 on 2022-09-06 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('epic_events', '0007_alter_user_password_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='contract',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='epic_events.contract'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contract',
            name='payment_due',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epic_events.statusevent'),
        ),
    ]
