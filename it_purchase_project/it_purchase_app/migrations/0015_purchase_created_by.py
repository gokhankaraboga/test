# Generated by Django 2.0.5 on 2018-06-05 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it_purchase_app', '0014_auto_20180605_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='created_by',
            field=models.CharField(default='', max_length=500),
        ),
    ]