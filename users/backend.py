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


    def authenticate(self, mobile, otp, user_type):
        try:
            user = User.objects.get(
                mobile=mobile, is_active=True, is_deleted=False, user_type=user_type
            )
        except User.DoesNotExist:
            return None

        return user if user.confirm_otp(otp, Tokens.TOKEN_TYPE.LOGIN) else None