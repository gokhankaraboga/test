# Generated by Django 2.0.5 on 2018-06-07 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it_purchase_app', '0028_auto_20180607_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='price_quoted',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
