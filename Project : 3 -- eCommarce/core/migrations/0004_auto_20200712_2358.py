# Generated by Django 2.2.12 on 2020-07-12 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200712_2351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='lebel',
            new_name='label',
        ),
    ]