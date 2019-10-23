import uuid

from django.db import models
# from django.contrib.gis.db.models import PointField
from django.template.defaultfilters import slugify
from django.utils import timezone

from model_utils import Choices

import users.models


class Merchant(models.Model):
    merchant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant_address = models.ForeignKey(users.models.Addresses, on_delete=models.CASCADE)
    merchant_slug = models.SlugField(unique=True, max_length=255, null=False)
    merchant_head = models.ManyToManyField(users.models.User)
    merchant_name = models.CharField(max_length=255, db_index=True)
    merchant_contact = models.IntegerField(db_index=True)
    merchant_email = models.EmailField(db_index=True)
    using_our_db = models.BooleanField(default=False, db_index=True,
                                       verbose_name=u"Merchan Using Our DB")
    other_details = models.TextField()
    other = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    added_by = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True,
                                 related_name="merchant_added_by",)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "{} - {}".format(self.merchant_name, self.merchant_email)

    class Meta:
        verbose_name = "Merchant"
        verbose_name_plural = "Merchants"

    def save(self, *args, **kwargs):
        if not self.merchant_id:
            self.store_slug = slugify(self.merchant_name)

        super(Merchant, self).save(*args, **kwargs)


class MerchantCategory(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=255)
    category_slug = models.SlugField()
    added_by = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True,
                                 related_name="category_added_by", )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "Store Category"
        verbose_name_plural = "Store Categories"

    def save(self, *args, **kwargs):
        if not self.category_id:
            self.store_slug = slugify(self.category_name)

        super(MerchantCategory, self).save(*args, **kwargs)


class Store(models.Model):
    STORE_SIZE = Choices(
        (0, 'SMALL', 'SMALL'),
        (1, 'MID', 'MID'),
        (2, 'LARGE', 'LARGE')
    )
    store_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    store_category = models.ManyToManyField(MerchantCategory)
    store_address = models.ForeignKey(users.models.Addresses, on_delete=models.CASCADE)
    store_latitude = models.CharField(max_length=255)
    store_longitude = models.CharField(max_length=255)
    store_size = models.IntegerField(choices=STORE_SIZE, default=STORE_SIZE.SMALL)
    # store_location = models.PointField()
    store_map_url = models.URLField()

    store_head = models.ManyToManyField(users.models.User)
    store_slug = models.SlugField(unique=True, max_length=255, null=False)
    store_name = models.CharField(max_length=255, db_index=True)
    store_contact = models.IntegerField(db_index=True)
    store_email = models.EmailField(db_index=True)
    is_approved = models.BooleanField(default=False, db_index=True)
    provide_delivery = models.BooleanField(default=False, db_index=True)
    min_delivery_payment = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    delivery_charges = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    other = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False, db_index=True)
    added_by = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True,
                                 related_name="store_added_by",)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.store_name, self.store_email)

    class Meta:
        verbose_name = "Merchant Store"
        verbose_name_plural = "Merchant Stores"

    def save(self, *args, **kwargs):
        if not self.store_id:
            self.store_slug = '-'.join((slugify(self.store_name), slugify(self.merchant.merchant_name)))

        super(Store, self).save(*args, **kwargs)


class MerchantAccessKeys(models.Model):
    merchant = models.OneToOneField(Merchant, on_delete=models.CASCADE)
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
    access_key = models.CharField(unique=True, max_length=255, db_index=True)
    secret_key = models.CharField(unique=True, max_length=255, db_index=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return None

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"


class MerchantWebsiteAPI(models.Model):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4
    PATCH = 5
    METHODS = ((GET, 'GET'),
               (POST, 'POST'),
               (PUT, 'PUT'),
               (DELETE, 'DELETE'),
               (PATCH, 'PATCH'))

    PRODUCT_DETAILS = 1
    PRODUCTS_LIST = 2
    PAYMENT_UPDATE = 3
    API_USE = ((PRODUCT_DETAILS, 'PRODUCT'),
               (PRODUCTS_LIST, 'PRODUCTS'),
               (PAYMENT_UPDATE, 'PAYMENT'))
    merchant = models.OneToOneField(Merchant, on_delete=models.CASCADE)
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
    access_key = models.CharField(unique=True, max_length=255, db_index=True)
    secret_key = models.CharField(unique=True, max_length=255, db_index=True)
    api_url = models.URLField()
    method = models.IntegerField(default=GET, choices=METHODS, db_index=True)
    api_use = models.IntegerField(default=PRODUCT_DETAILS, choices=API_USE, db_index=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return None

    class Meta:
        verbose_name = "Merchants API"
        verbose_name_plural = "Merchants API"


class MerchantEmployees(models.Model):

    MANAGER = 1
    ASST_MANAGER = 2
    SALESMAN = 3
    BILLING = 4
    OTHER = 5
    ROLES = ((MANAGER, 'Manager'),
             (ASST_MANAGER, 'Asst. Manager'),
             (SALESMAN, 'Salesman'),
             (BILLING, 'Billing'),
             (OTHER, 'Other'))

    emp_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(users.models.User, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    role = models.IntegerField(default=OTHER, choices=ROLES, db_index=True)
    other = models.CharField(max_length=255)
    added_by = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True,
                                 related_name="emp_added_by")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.user.name, self.user.email)

    class Meta:
        verbose_name = "Merchant User"
        verbose_name_plural = "Merchant Users"


class MerchantCoupons(models.Model):
    """
    This is for coupons through COUPONS, 
    - Coupons can be redeemed to specific merchants, stores, user and between specific dates.
    - Merchants can created COUPONS for their level discounts
    """
    PERCENT = 1
    FLAT = 2
    DISCOUNT_TYPE = ((PERCENT, 'Percent'),
                     (FLAT, 'Flat'))
    coupon_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ManyToManyField(users.models.User)
    coupon_code = models.CharField(max_length=50, unique=True)
    min_price_for_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0, db_index=True)
    max_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0, db_index=True, verbose_name=u"In Flat Rupee")
    discount_type = models.IntegerField(default=PERCENT, choices=DISCOUNT_TYPE, db_index=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2,  default=0.0)
    available_after = models.DateTimeField(null=False, db_index=True)
    expire_before = models.DateTimeField(null=False, db_index=True)
    is_available = models.BooleanField(default=True, db_index=True)
    discount_by_merchant = models.BooleanField(default=True, verbose_name=u"Discount Given by Merchant")
    added_by = models.ForeignKey(users.models.User,on_delete=models.CASCADE,
                                 null=True, related_name="merchant_coupon_added_by")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.coupon_code

    class Meta:
        verbose_name = "Product Offers"
        verbose_name_plural = "Products Offers"


class MerchantOffers(models.Model):
    """
    This is for Promotional Offers only, not for discount and all
    """
    offer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='offers/images/')
    offer_details = models.TextField()
    available_after = models.DateTimeField(null=False, db_index=True)
    expire_before = models.DateTimeField(null=False, db_index=True)
    is_available = models.BooleanField(default=True, db_index=True)
    added_by = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.offer_id

    class Meta:
        verbose_name = "Merchant Offer"
        verbose_name_plural = "Merchant Offers"
