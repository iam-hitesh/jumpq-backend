import uuid
import datetime

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone
from django.conf import settings

from model_utils import Choices
import pyotp

import users.constants
import users.messages
import common.helpers


class CustomAccountManager(BaseUserManager):
    def create_user(self, mobile, password):
        user = self.model(mobile=mobile, password=password)
        user.set_password(password)
        user.is_active = False
        user.is_staff = False
        user.is_superuser = False
        user.referral_code = common.helpers.generate_referral_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password):
        user = self.create_user(mobile=mobile, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.user_type = User.ACCOUNT_TYPE.ADMIN
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, mobile_):
        print(mobile_)
        return self.get(mobile=mobile_)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Here we are subclassing the Django AbstractBaseUser, which comes with only
    3 fields:
    1 - password
    2 - last_login
    3 - is_active
    Note than all fields would be required unless specified otherwise, with
    `required=False` in the parentheses.
    The PermissionsMixin is a model that helps you implement permission settings
    as-is or modified to your requirements.
    More info: https://goo.gl/YNL2ax
    """

    DEFAULT_LANG = Choices(
        (1, 'ENGLISH', 'English'),
        (2, 'HINDI', 'Hindi'))

    ACCOUNT_TYPE = Choices(
        (1, 'ADMIN', 'Admin'),
        (2, 'MERCHANT', 'Merchant'),
        (3, 'CUSTOMER', 'Customer'))

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, default='', null=True,
                            verbose_name=u"Name of User", db_index=True)
    mobile = models.CharField(max_length=15, default=0, unique=True,
                              verbose_name=u"Mobile Number", db_index=True)
    email = models.EmailField(unique=True, db_index=True, null=True)
    default_lang = models.IntegerField(default=DEFAULT_LANG.ENGLISH, choices=DEFAULT_LANG)
    user_type = models.IntegerField(default=ACCOUNT_TYPE.CUSTOMER, choices=ACCOUNT_TYPE)
    is_staff = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=False, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    profile_pic = models.ImageField(upload_to='users/profile_pics/', default='default.jpg')
    referral_code = models.CharField(max_length=30, default='', null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    # REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'mobile'

    objects = CustomAccountManager()

    def get_short_name(self):
        return self.name

    def natural_key(self):
        return self.email

    def __str__(self):
        return "{} - {}".format(self.name, self.mobile)

    class Meta:
        ordering = ('mobile',)
        verbose_name = 'User profile'
        verbose_name_plural = 'User Profile'

    def confirm_otp(self, otp, token_type):
        token = Tokens.objects.filter(
            expire_on__gte=timezone.now(),
            user=self,
            token_type=token_type,
            is_used=False
        )

        if otp == token.last().token:
            token.update(is_used=True)
            return True
        else:
            return False


    @classmethod
    def send_otp(cls, mobile, referral_code=None):
        user = User.objects.filter(mobile=mobile)

        if not user.exists():

            user = User.objects.create(
                mobile=mobile,
                referral_code=common.helpers.generate_referral_code()
            )
        else:
            user = user.last()

        token = Tokens.objects.filter(
            expire_on__gte=timezone.now(),
            user=user,
            token_type=Tokens.TOKEN_TYPE.LOGIN,
            is_used=False
        )

        if token.exists():
            token = token.last()
        else:
            get_token = pyotp.TOTP(settings.OTP_SECRET)
            # get_token = get_token.now()
            get_token = 123456
            token = Tokens.objects.create(
                user=user,
                token=get_token,
                token_type=Tokens.TOKEN_TYPE.LOGIN
            )

        message_text = users.messages.LOGIN_OTP_MSG % token

        # Asynchronously send OTP SMS
        common.helpers.send_sms.apply_async(
            args=[mobile, message_text], countdown=0.5)

        return True

    def save(self, *args, **kwargs):
        mobile = kwargs.pop('mobile', False)
        user = User.objects.filter(mobile=mobile)

        if not self.pk and user:
            self.user = user.first()
            self.token_type = Tokens.LOGIN
            self.token = '123456'
            self.is_used = False
            self.expire_on = timezone.now() + datetime.timedelta(minutes=20)

        super(User, self).save(*args, **kwargs)


class Tokens(models.Model):
    TOKEN_TYPE = Choices(
        (0, 'EMAIL_CONFIRMATION', 'Email Confirmation'),
        (1, 'MOBILE_CONFIRMATION', 'Mobile Confirmation'),
        (2, 'FORGOT_PASSWORD', 'Forgot Password'),
        (3, 'LOGIN', 'Login'),
        (4, 'ORDER_CONFIRM', 'Order Confirm')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    token = models.CharField(max_length=250, null=False, db_index=True)
    token_type = models.IntegerField(default=TOKEN_TYPE.EMAIL_CONFIRMATION,
                                     choices=TOKEN_TYPE, db_index=True)
    is_used = models.BooleanField(default=False, db_index=True)
    expire_on = models.DateTimeField(default=timezone.now() + datetime.timedelta(minutes=30))
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.user.name, self.token)

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"


class Country(models.Model):
    country_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country_name = models.CharField(max_length=255, default='', null=False,
                                    db_index=True)
    alt_country_name = models.CharField(max_length=255, default='', null=False,
                                        db_index=True)
    iso = models.CharField(max_length=255, default='', null=False)
    country_code = models.CharField(max_length=255, default='', null=False,
                                    db_index=True)
    phone_code = models.IntegerField(default=91,
                                     db_index=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.country_name, self.country_code)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class State(models.Model):
    state_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.ForeignKey(Country, db_index=True, on_delete=models.CASCADE)
    state_name = models.CharField(max_length=255, default='', null=False,
                                  db_index=True)
    alt_state_name = models.CharField(max_length=255, default='', null=False,
                                      db_index=True)
    iso = models.CharField(max_length=255, default='', null=False)
    state_code = models.CharField(max_length=255, default='', null=False,
                                  db_index=True)
    phone_code = models.IntegerField(default=91, null=True,
                                     db_index=True)
    currency = models.CharField(max_length=50, default="INR")
    currency_sign = models.CharField(max_length=50, default="₹")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.state_name, self.country.name)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class City(models.Model):
    state = models.ForeignKey(State, db_index=True, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=255, default='', null=False,
                                 db_index=True)
    alt_city_name = models.CharField(max_length=255, default='', null=False,
                                     db_index=True)
    iso = models.CharField(max_length=255, default='', null=False)
    city_code = models.CharField(max_length=255, default='', null=False,
                                 db_index=True)
    phone_code = models.IntegerField(default=91, null=True,
                                     db_index=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.city_name, self.state.name)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"


class Addresses(models.Model):
    """

    """
    HOME = 1
    OFFICE = 2
    OTHER = 3
    ADDRESS_TYPE = ((HOME, 'Home'),
                    (OFFICE, 'Office'),
                    (OTHER, 'Others'))
    address_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, db_index=True, on_delete=models.CASCADE)
    state = models.ForeignKey(State, db_index=True, on_delete=models.CASCADE)
    city = models.ForeignKey(City, db_index=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default='', null=False)
    landmark = models.CharField(max_length=255, default='', null=True)
    pincode = models.CharField(max_length=255, default='', null=False)
    location = models.CharField(max_length=255, default='', null=True)
    map_location = models.TextField()
    mobile = models.IntegerField()
    address_type = models.IntegerField(default=HOME, choices=ADDRESS_TYPE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "Addresses"
        verbose_name_plural = "Address"