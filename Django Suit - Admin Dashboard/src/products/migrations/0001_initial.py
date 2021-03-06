# Generated by Django 2.1.2 on 2020-12-10 14:51

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import products.models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='category/image/')),
                ('slug', models.SlugField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('mptt_level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.Category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalProducts',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(default='Default title !!!', max_length=450)),
                ('image', models.TextField(blank=True, max_length=500, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Product Price')),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Discount Price')),
                ('slug', models.SlugField(blank=True)),
                ('description', models.TextField(null=True)),
                ('additional_info', models.TextField(null=True)),
                ('product_code', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('modified', models.DateTimeField(blank=True, editable=False)),
                ('average_rate', models.FloatField(blank=True, default=0, null=True)),
                ('status', models.CharField(choices=[('In Stock', 'In Stock'), ('StockOut', 'StockOut'), ('Unknown', 'Unknown')], default='In Stock', max_length=30, null=True)),
                ('label', models.CharField(choices=[('New', 'New'), ('Hot', 'Hot'), ('Bestselling', 'Bestselling')], max_length=20)),
                ('featured', models.BooleanField(default=False, verbose_name='Featured Product')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('category', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='product', to='products.Category')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical products',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, max_length=500, null=True, upload_to=products.models.image_upload_path)),
                ('short_description', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Default title !!!', max_length=450)),
                ('image', models.ImageField(blank=True, max_length=500, null=True, upload_to=products.models.image_upload_path)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Product Price')),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Discount Price')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField(null=True)),
                ('additional_info', models.TextField(null=True)),
                ('product_code', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('average_rate', models.FloatField(blank=True, default=0, null=True)),
                ('status', models.CharField(choices=[('In Stock', 'In Stock'), ('StockOut', 'StockOut'), ('Unknown', 'Unknown')], default='In Stock', max_length=30, null=True)),
                ('label', models.CharField(choices=[('New', 'New'), ('Hot', 'Hot'), ('Bestselling', 'Bestselling')], max_length=20)),
                ('featured', models.BooleanField(default=False, verbose_name='Featured Product')),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='cat_products', related_query_name='product', to='products.Category')),
            ],
            options={
                'verbose_name_plural': 'Products',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=250)),
                ('rate', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', related_query_name='review', to='products.Products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', related_query_name='review', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductsExtraImages', related_query_name='extraimages', to='products.Products'),
        ),
    ]
