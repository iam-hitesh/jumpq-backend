from django.db.models import Q

from rest_framework import permissions

from .models import *


class UserAuthentication(object):
    """
    This authentication method is used for adding more check during user loogging
    """

    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False


    def get_user(self, user_id):
       try:
          return User.objects.get(pk=user_id)
       except User.DoesNotExist:
          return None


    def authenticate(self, mobile, otp, user_type=None):
        try:
            user = User.objects.get(
                Q(user_type=User.ACCOUNT_TYPE.MERCHANT) | Q(user_type=User.ACCOUNT_TYPE.CUSTOMER),
                mobile=mobile, is_active=True, is_deleted=False
            )
        except User.DoesNotExist:
            return None

        return user if user.confirm_otp(otp, Tokens.TOKEN_TYPE.LOGIN) else None


class IsMerchant(permissions.BasePermission):
    """
    Global permission check for Merchant Users
    """

    def has_permission(self, request, view):
        return request.user.user_type == User.ACCOUNT_TYPE.MERCHANT


class IsCustomer(permissions.BasePermission):
    """
    Global permission check for customer Users
    """

    def has_permission(self, request, view):
        return request.user.user_type == User.ACCOUNT_TYPE.CUSTOMER