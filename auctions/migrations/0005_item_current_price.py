# Generated by Django 3.1.3 on 2020-11-25 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20201125_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='current_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]
