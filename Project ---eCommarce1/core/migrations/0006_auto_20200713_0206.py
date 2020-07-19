# Generated by Django 2.2.12 on 2020-07-12 20:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_auto_20200713_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Discount Price'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='Products/%Y/%m/%d/', verbose_name='2nd Image'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='Products/%Y/%m/%d/', verbose_name='3rd Image'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='Products/%Y/%m/%d/', verbose_name='4th Image'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Product Price'),
        ),
        migrations.CreateModel(
            name='HistoricalItem',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(default='Default title !!!', max_length=450)),
                ('image', models.TextField(blank=True, default='ProductsDefault.jpg', max_length=100, null=True, verbose_name='Main Image')),
                ('image1', models.TextField(blank=True, max_length=100, null=True, verbose_name='2nd Image')),
                ('image2', models.TextField(blank=True, max_length=100, null=True, verbose_name='3rd Image')),
                ('image3', models.TextField(blank=True, max_length=100, null=True, verbose_name='4th Image')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Product Price')),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Discount Price')),
                ('slug', models.SlugField(blank=True)),
                ('summary', models.CharField(default='Default Summary !!!', max_length=450)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('S', 'Shirt'), ('SW', 'Sports Wear'), ('OW', 'Out Wear')], max_length=2)),
                ('label', models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger')], max_length=1)),
                ('featured', models.BooleanField(default=False, verbose_name='Featured Product')),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('modified', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical item',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
