# Generated by Django 2.2.12 on 2020-05-16 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='demo_profile.jpeg', upload_to='profile_picture/%Y/%m/%d/'),
        ),
    ]
