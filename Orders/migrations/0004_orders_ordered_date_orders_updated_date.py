# Generated by Django 4.2.2 on 2023-06-12 03:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0003_remove_orders_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='ordered_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
