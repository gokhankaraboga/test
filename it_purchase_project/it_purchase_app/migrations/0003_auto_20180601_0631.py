# Generated by Django 2.0.5 on 2018-06-01 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it_purchase_app', '0002_supportcomment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SupportComment',
        ),
        migrations.AddField(
            model_name='purchase',
            name='support_comment',
            field=models.CharField(default='', max_length=500),
        ),
    ]
