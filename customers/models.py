import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

import users.models
import merchants.models
import products.models

class Customer(models.Model):
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(users.models.User, on_delete=models.CASCADE)
    referred_by = models.ForeignKey(users.models.User, related_name="referral",
                                    on_delete=models.CASCADE, null=True)
    jumpq_points = models.IntegerField(default=0)
    added_by = models.ForeignKey(users.models.User, related_name="added_by",
                                 on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.mobile

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    merchant = models.ForeignKey(merchants.models.Merchant, on_delete=models.CASCADE)
    store = models.ForeignKey(merchants.models.Store, on_delete=models.CASCADE)
    product = models.ForeignKey(products.models.ProductDetail, on_delete=models.CASCADE)
    offer = models.ForeignKey(products.models.ProductOffer, on_delete=models.CASCADE)
    offer_applied = models.BooleanField(default=False)
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    state_gst = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, verbose_name=u"In Rupee")
    central_gst = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, verbose_name=u"In Rupee")
    is_paid = models.BooleanField(default=False, db_index=True)
    is_deleted = models.BooleanField(default=False,db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.user.id

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Cart"


# class FavoriteProducts(models.Model):
