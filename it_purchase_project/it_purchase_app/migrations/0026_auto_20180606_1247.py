# Generated by Django 2.0.5 on 2018-06-06 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it_purchase_app', '0025_auto_20180606_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='need_price_quote',
            field=models.BooleanField(default=False),
        ),
    ]