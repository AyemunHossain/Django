# Generated by Django 2.1.5 on 2020-02-08 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_title', models.CharField(max_length=200)),
                ('news_author', models.CharField(max_length=50)),
                ('news_content', models.TextField()),
                ('news_published', models.DateTimeField()),
            ],
        ),
    ]
