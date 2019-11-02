from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.http import JsonResponse

from rest_framework.views import APIView
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

from merchants import models


longitude = 7.209023
latitude = 8.613939

user_location = Point(longitude, latitude, srid=4326)


class NearbyStores(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        queryset = models.Store.objects.annotate(distance=Distance('store_location', user_location)).order_by('distance')

        return JsonResponse({'resp_code': queryset[0].distance},
                            status=HTTP_400_BAD_REQUEST)