# Generated by Django 2.0.5 on 2018-06-05 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it_purchase_app', '0011_remove_purchase_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='created_by',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='purchase',
            name='manager_username',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='purchase',
            name='purchase_username',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='purchase',
            name='support_username',
            field=models.CharField(default='', max_length=500),
        ),
    ]
