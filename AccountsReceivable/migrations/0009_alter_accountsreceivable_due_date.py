# Generated by Django 4.2.2 on 2023-06-15 18:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccountsReceivable', '0008_alter_accountsreceivable_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountsreceivable',
            name='due_date',
            field=models.DateField(default=datetime.date(2023, 7, 15)),
        ),
    ]
