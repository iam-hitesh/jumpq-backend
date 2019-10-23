import uuid
from decimal import Decimal

from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

from model_utils import Choices

import users.models
import merchants.models


class ProductCategory(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=255, null=False)
    sub_category_name = models.CharField(max_length=255, null=False)
    category_slug = models.SlugField(max_length=255, unique=True)
    other = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False, db_index=True)
    added_by = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Produc Categories"

    def save(self, *args, **kwargs):
        if not self.category_id:
            self.category_slug = '-'.join((slugify(self.category_name), slugify(self.sub_category_name)))

        super(ProductCategory, self).save(*args, **kwargs)

class ProductImages(models.Model):
    name = models.CharField(max_length=255)
    size = models.IntegerField(verbose_name=u"In KB")
    format = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/images/')
    is_deleted = models.BooleanField(default=False, db_index=True)
    added_by = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"


class Product(models.Model):
    METRIC_SYSTEM = Choices(
        (0, 'KG', 'KG'),
        (1, 'METRE', 'Metre'),
        (2, 'LITRE', 'Litre'),
        (3, 'DOZEN', 'Dozen'),
        (4, 'QUANTITY', 'Quantity'),
        (5, 'UNKNOWN', 'Unknown'))
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    category = models.ManyToManyField(ProductCategory, verbose_name=u"Product Categories")
    product_name = models.CharField(max_length=255, db_index=True)
    product_desc = models.TextField()
    product_image = models.ManyToManyField(ProductImages)
    manufacturer = models.CharField(max_length=255, db_index=True)
    manufacturer_details = models.TextField()
    metric_system = models.IntegerField(default=METRIC_SYSTEM.QUANTITY, choices=METRIC_SYSTEM)
    product_slug = models.CharField(max_length=255)
    other = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False, db_index=True)
    added_by = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.product_slug = '-'.join((slugify(self.product_name), slugify(self.manufacturer)))

        super(Product, self).save(*args, **kwargs)

class ProductAttribute(models.Model):
    attribute_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    attribute_name = models.CharField(max_length=255, default='')
    added_by = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.attribute_name

    class Meta:
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"


class ProductAttributeValue(models.Model):
    attr_value_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, default='')
    added_by = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.attribute_name

    class Meta:
        verbose_name = "Product Attribute Value"
        verbose_name_plural = "Product Attribute Values"


class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    merchant = models.ForeignKey(merchants.models.Merchant, on_delete=models.CASCADE)
    store = models.ForeignKey(merchants.models.Store, on_delete=models.CASCADE)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, null=False, verbose_name=u"Tax Exclusive")
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, null=False, verbose_name=u"Tax Exclusive")

    # Sale Price
    sale_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, null=False, verbose_name=u"Tax Inclusive")
    sale_from = models.DateTimeField(verbose_name=u"Sale start", blank=True, null=True)
    sale_to = models.DateTimeField(verbose_name="Sale end", blank=True, null=True)
    is_tax_inclusive = models.BooleanField(default=True)
    state_gst = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, verbose_name=u"In percent")
    central_gst = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, verbose_name=u"In Percent")
    merchant_product_id = models.CharField(max_length=255, null=True)

    # Attribute like Size, Color, and Other ISBN All Details
    attribute = models.ManyToManyField(ProductAttributeValue)

    # Quantity of the Product with respect to that Attribute
    quantity = models.IntegerField(default=0, null=False)

    other_details = models.TextField(help_text=u"Other Product Related Details")
    is_available = models.BooleanField(default=True, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    added_by = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "Product Details"
        verbose_name_plural = "Products Details"

    def on_sale(self):
        """
        Returns True if the sale price is applicable.
        """
        now = timezone.now()
        valid_from = self.sale_from is None or self.sale_from < now
        valid_to = self.sale_to is None or self.sale_to > now
        return self.sale_price is not None and valid_from and valid_to

    def discount_price(self):
        return self.discounted_price is not None

    def price(self):
        """
        Returns the actual price - sale price if applicable otherwise
        the unit price.
        """
        if self.on_sale():
            return self.sale_price
        elif self.discount_price():
            return self.discounted_price
        return Decimal(self.original_price)


class ProductOffer(models.Model):
    DISCOUNT_TYPE = Choices(
        (0, 'PERCENT', 'Percent'),
        (1, 'FLAT', 'Flat'))
    offer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    merchant = models.ForeignKey(merchants.models.Merchant, on_delete=models.CASCADE)
    store = models.ForeignKey(merchants.models.Store, on_delete=models.CASCADE)
    discount_type = models.IntegerField(default=DISCOUNT_TYPE.PERCENT, choices=DISCOUNT_TYPE, db_index=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    min_quantity = models.IntegerField(verbose_name=u"Minimum Product Quantity to apply Offer")
    coupon_code = models.CharField(max_length=50, unique=True, db_index=True)
    available_after = models.DateTimeField(null=False, db_index=True)
    expire_before = models.DateTimeField(null=False, db_index=True)
    is_available = models.BooleanField(default=True, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    added_by = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.coupon_code

    class Meta:
        verbose_name = "Product Offers"
        verbose_name_plural = "Products Offers"