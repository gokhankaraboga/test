# Generated by Django 2.0.5 on 2018-06-05 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('it_purchase_app', '0012_auto_20180605_0707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='manager_username',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='purchase_username',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='support_username',
        ),
    ]
