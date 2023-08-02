# Generated by Django 4.2.3 on 2023-08-02 00:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0001_initial'),
        ('Items', '0001_initial'),
        ('Orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='items',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orderitem', to='Items.items'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='orders',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='_orderitem', to='Orders.orders'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='customers',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='Customers.customers'),
            preserve_default=False,
        ),
    ]
