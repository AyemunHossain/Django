# Generated by Django 2.1.5 on 2020-03-26 17:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorials',
            name='tutorial_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 26, 17, 38, 15, 846966), verbose_name='Published Date'),
        ),
    ]