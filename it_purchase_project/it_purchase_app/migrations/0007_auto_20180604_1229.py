# Generated by Django 2.0.5 on 2018-06-04 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it_purchase_app', '0006_auto_20180604_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='need_price_quote',
            field=models.BooleanField(default=False, verbose_name='Price Quote Required'),
        ),
    ]
