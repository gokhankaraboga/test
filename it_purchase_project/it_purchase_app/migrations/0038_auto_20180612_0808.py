# Generated by Django 2.0.5 on 2018-06-12 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('it_purchase_app', '0037_auto_20180612_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseitem',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='it_purchase_app.Purchase'),
        ),
    ]
