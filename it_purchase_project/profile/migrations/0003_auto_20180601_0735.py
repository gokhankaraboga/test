# Generated by Django 2.0.5 on 2018-06-01 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_auto_20180531_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='job_title',
            field=models.CharField(blank=True, choices=[('developer', 'Developer'), ('manager', 'Manager'), ('support', 'Support')], max_length=250),
        ),
    ]