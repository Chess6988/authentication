# Generated by Django 5.0.3 on 2024-12-17 10:33

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camions', '0005_alter_rubbertransport_tons_of_rubber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rubbertransport',
            name='number_of_trucks',
        ),
        migrations.AddField(
            model_name='rubbertransport',
            name='recette',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15),
        ),
    ]
