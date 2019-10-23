import json

from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_502_BAD_GATEWAY
)
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings


from .backend import UserAuthentication
from users.models import *
import users.constants
import users.forms
from .constants import *
from .serializers import *


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class SendOTP(APIView):
    """
    This class will be use to send OTP on given Phone Number is registered or Not Registered.
    """

    permission_classes = (AllowAny, )

    def get(self, request):
        """
        Will send OTP on given mobile number
        :param request: 
        :return: status
        """

        mobile = request.GET.get('mobile', None)
        referral_code = request.GET.get('referral', None)
        form = users.forms.OTPForm(request.GET)

        if not form.is_valid():
            return JsonResponse({'resp_code': ERROR_RESP_CODE, 'message': form.errors},
                                status=HTTP_400_BAD_REQUEST)

        otp_sent = User.send_otp(mobile, referral_code)

        if otp_sent:
            return JsonResponse({'resp_code': SUCCESS_RESP_CODE, 'message': 'Login OTP Sent'},
                                status=HTTP_201_CREATED)
        else:
            return JsonResponse({'resp_code': 0, 'message': 'Some Error Occurred'},
                                status=HTTP_400_BAD_REQUEST)



class MerchantLogin(APIView):
    """
    This class will be login user and generating Token for API Authentication, 
    this will have public access(as anyone open to login this)
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        """
        post method
        :param request: 
        :return: 
        """

        try:
            data = json.loads(request.body)
            mobile = data['mobile']
            otp = data['otp']

            # Call UserAuthentication class from backends.py file for custom
            # authentication checks
            Auth = UserAuthentication()
            user = Auth.authenticate(mobile=mobile, otp=otp, user_type=User.ACCOUNT_TYPE.ADMIN)

            if not user:
                return JsonResponse({'resp_code': 0, 'message': 'Invalid Credentials'},
                                    status=HTTP_400_BAD_REQUEST)

            try:
                # This is will generate a token for authentication
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                user = User.objects.get(mobile=mobile)
                user_data = UserSerializer(user, many=False)

                return JsonResponse({'resp_code': 1,'message':'Login successful',
                                     'token': token, 'profile':user_data.data}, status=HTTP_202_ACCEPTED)
            except:
                return JsonResponse({'resp_code': 0,
                                     'message': 'can not authenticate with the '
                                                'given credentials or the account '
                                                'has been deactivated'},
                                    status=HTTP_400_BAD_REQUEST)

        except KeyError:
            # If any key is missing during sending the data
            return JsonResponse({'resp_code': 0, 'message': 'please provide a '
                                                         'phone number and a OTP'},
                                status=HTTP_400_BAD_REQUEST)
        except Exception:
            return JsonResponse({'resp_code': 0, 'message': 'Some Error Occurred'},
                                status=HTTP_400_BAD_REQUEST)


class CustomerLogin(APIView):
    """
    This class will be login user and generating Token for API Authentication, 
    this will have public access(as anyone open to login this)
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        """
        post method
        :param request: 
        :return: 
        """

        try:
            data = json.loads(request.body)
            mobile = data['mobile']
            otp = data['otp']

            # Call UserAuthentication class from backends.py file for custom
            # authentication checks
            Auth = UserAuthentication()
            user = Auth.authenticate(mobile=mobile, otp=otp, user_type=User.ACCOUNT_TYPE.ADMIN)

            if not user:
                return JsonResponse({'resp_code': 0, 'message': 'Invalid Credentials'},
                                    status=HTTP_400_BAD_REQUEST)

            try:
                # This is will generate a token for authentication
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                user = User.objects.get(mobile=mobile)
                user_data = UserSerializer(user, many=False)

                return JsonResponse({'resp_code': 1,'message':'Login successful',
                                     'token': token, 'profile':user_data.data}, status=HTTP_202_ACCEPTED)
            except:
                return JsonResponse({'resp_code': 0,
                                     'message': 'can not authenticate with the '
                                                'given credentials or the account '
                                                'has been deactivated'},
                                    status=HTTP_400_BAD_REQUEST)

        except KeyError:
            # If any key is missing during sending the data
            return JsonResponse({'resp_code': 0, 'message': 'please provide a '
                                                         'phone number and a password'},
                                status=HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'},
                                status=HTTP_400_BAD_REQUEST)
