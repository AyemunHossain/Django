# Generated by Django 2.2.12 on 2020-07-20 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_refund_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
