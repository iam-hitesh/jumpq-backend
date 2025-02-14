# Generated by Django 2.2.6 on 2019-11-02 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('merchants', '0002_auto_20191102_1737'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productoffer',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productoffer',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchants.Merchant'),
        ),
        migrations.AddField(
            model_name='productoffer',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
        migrations.AddField(
            model_name='productoffer',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchants.Store'),
        ),
        migrations.AddField(
            model_name='productimages',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productdetail',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productdetail',
            name='attribute',
            field=models.ManyToManyField(to='products.ProductAttributeValue'),
        ),
        migrations.AddField(
            model_name='productdetail',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchants.Merchant'),
        ),
        migrations.AddField(
            model_name='productdetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
        migrations.AddField(
            model_name='productdetail',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchants.Store'),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productattributevalue',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productattributevalue',
            name='attribute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ProductAttribute'),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(to='products.ProductCategory', verbose_name='Product Categories'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ManyToManyField(to='products.ProductImages'),
        ),
    ]
