# Generated by Django 4.2.2 on 2023-06-09 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0003_alter_items_price_accountspayable'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AccountsPayable',
            new_name='Invoices',
        ),
    ]
