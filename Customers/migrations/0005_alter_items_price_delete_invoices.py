# Generated by Django 4.2.2 on 2023-06-09 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0004_rename_accountspayable_invoices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='price',
            field=models.FloatField(),
        ),
        migrations.DeleteModel(
            name='Invoices',
        ),
    ]