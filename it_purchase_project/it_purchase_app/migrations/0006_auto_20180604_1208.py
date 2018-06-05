# Generated by Django 2.0.5 on 2018-06-04 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it_purchase_app', '0005_remove_purchaseprocess_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='manager_approved',
            field=models.BooleanField(default=False, verbose_name='Approved'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='manager_comment',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='purchase',
            name='need_price_quote',
            field=models.BooleanField(default=False, verbose_name='Approved'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='purchase_team_comment',
            field=models.CharField(default='', max_length=500),
        ),
    ]
