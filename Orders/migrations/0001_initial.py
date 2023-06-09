# Generated by Django 4.2.2 on 2023-06-09 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Items', '0001_initial'),
        ('Customers', '0010_remove_accountsreceivable_order_delete_logmessage_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customers.customers')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Items.items')),
            ],
        ),
    ]
