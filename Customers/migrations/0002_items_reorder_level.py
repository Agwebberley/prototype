# Generated by Django 4.2.2 on 2023-06-08 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='reorder_level',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]