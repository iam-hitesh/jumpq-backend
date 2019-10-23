import uuid

from django.utils import timezone
from django.db import models

import users.models
import merchants.models
import customers.models


class Orders(models.Model):

    CASH = 1
    CARD = 2
    NET_BANKING = 3
    UPI = 4
    OTHER = 5
    PAYMENT_TYPE = ((CASH,'Cash'),
                    (CARD, 'Card'),
                    (NET_BANKING, 'Net Banking'),
                    (UPI, 'UPI'),
                    (OTHER,'Other'))

    PICKUP = 1
    HOME_DELIVERY = 2
    STORE = 3
    DELIVERY_TYPE = ((PICKUP, 'Pickup'),
                     (HOME_DELIVERY, 'Home Devlivery'),
                     (STORE, 'Store'))

    PENDING = 1
    PLACED = 2
    PAID = 3
    IN_TRANSACTION = 4
    WAITING = 5
    DELIVERED = 6
    RETURNED = 7
    DECLINED = 8
    FEEDBACK = 9
    ORDER_STATUS = ((PENDING, 'Pending'),
                    (PLACED, 'Placed'),
                    (PAID, 'Paid'),
                    (IN_TRANSACTION, 'In Transaction'),
                    (WAITING, 'Waiting'),
                    (DELIVERED, 'Delivered'),
                    (RETURNED, 'Returned'),
                    (DECLINED, 'Declined'),
                    (FEEDBACK, 'Feedback Accepted'))

    offer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    items = models.ManyToManyField(customers.models.Cart)
    customer = models.ForeignKey(customers.models.Customer, on_delete=models.CASCADE)
    merchant = models.ForeignKey(merchants.models.Merchant, on_delete=models.CASCADE)
    store = models.ForeignKey(merchants.models.Store, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    state_gst = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, verbose_name=u"In Rupee")
    central_gst = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, verbose_name=u"In Rupee")
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    address = models.ForeignKey(users.models.Addresses, on_delete=models.CASCADE)
    pickup_otp = models.IntegerField()
    mobile_no = models.IntegerField(db_index=True)
    payment_type = models.IntegerField(default=CARD, choices=PAYMENT_TYPE)
    delivery_type = models.IntegerField(default=STORE, choices=DELIVERY_TYPE)
    order_status = models.IntegerField(default=PENDING, choices=ORDER_STATUS)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.offer_id

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class Payments(models.Model):

    INR = 1
    OTHER = 2
    CURRENCY = ((INR, 'INR'),
                (OTHER, 'OTHER'))

    TXN_PENDING = 1
    TXN_SUCCESS = 2
    TXN_FAILURE = 3
    TXN_STATUS = ((TXN_PENDING, 'Pending'),
                  (TXN_SUCCESS, 'Success'),
                  (TXN_FAILURE, 'Failed'))
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    customer = models.ForeignKey(customers.models.Customer, on_delete=models.CASCADE)
    merchant = models.ForeignKey(merchants.models.Merchant, on_delete=models.CASCADE)
    store = models.ForeignKey(merchants.models.Store, on_delete=models.CASCADE)
    currency = models.IntegerField(default=INR, choices=CURRENCY)
    txn_gateway_id = models.CharField(max_length=70)
    txn_bank_id = models.CharField(max_length=255)
    txn_status = models.IntegerField(default=TXN_PENDING, choices=TXN_STATUS)
    txn_gateway_name = models.CharField(max_length=20)
    txn_bank = models.TextField()
    txn_mode = models.CharField(max_length=20)
    txn_date = models.DateTimeField(null=False)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.payment_id

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"