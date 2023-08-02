# Generated by Django 4.2.3 on 2023-08-02 00:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0001_initial'),
        ('Items', '0001_initial'),
        ('Inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bin',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='_bin', to='Inventory.location'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bin_items',
            name='bin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='_bin_items', to='Inventory.bin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bin_items',
            name='items',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bin_items', to='Items.items'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='items',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='Items.items'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventoryhistory',
            name='inventory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='_inventoryhistory', to='Inventory.inventory'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventoryhistory',
            name='items',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='inventoryhistory', to='Items.items'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pick',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='_pick', to='Inventory.location'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pick',
            name='orders',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pick', to='Orders.orders'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pick_items',
            name='orderitem',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pick_items', to='Orders.orderitem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pick_items',
            name='pick',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='_pick_items', to='Inventory.pick'),
            preserve_default=False,
        ),
    ]
