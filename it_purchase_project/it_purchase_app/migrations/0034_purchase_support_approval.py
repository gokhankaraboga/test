# Generated by Django 2.0.5 on 2018-06-11 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it_purchase_app', '0033_auto_20180608_0802'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='support_approval',
            field=models.CharField(blank=True, choices=[('Not Decided', 'Not Decided'), ('Yes', 'Yes'), ('No', 'No')], max_length=500, null=True),
        ),
    ]