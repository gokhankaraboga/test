# Generated by Django 2.0.5 on 2018-06-06 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it_purchase_app', '0020_auto_20180606_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='price_quoted',
            field=models.FloatField(default=0.0),
        ),
    ]
