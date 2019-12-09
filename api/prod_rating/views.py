# python imports
import json
from datetime import datetime

# Django Imports
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from django.db.models import Count,Q,Sum,Avg
from django.db.models.functions import Coalesce


# Projects Imports
from libs.constants import (
		BAD_REQUEST,
		BAD_ACTION,
		OPERATION_NOT_ALLOWED,
)
# from accounts.constants import COULD_NOT_SEND_OTP, USER_NOT_REGISTERED
from libs.exceptions import (
					ParseException,
					ResourceNotFoundException,
				)

# app level imports
from .models import (
					rating,
					)
from .serialiser import (
	RatingAddSerializer,
	ListRatingSerializer,
)




class RateManager(GenericViewSet):
	# throttle_classes = (AnonRateThrottle,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']
	model = rating

	def get_queryset(self):
		return self.model.objects.all()

	serializers_dict = {
		'rateproduct': RatingAddSerializer,
		'ratelist': ListRatingSerializer,
		'getrate':ListRatingSerializer,
		}


	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)


	@action(methods=['post'], detail=False)
	def rateproduct(self, request, format='json'):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	@action(methods=['get'], detail=False)
	def ratelist(self, request, format='json'):
		page = self.paginate_queryset(self.get_queryset())
		serialiser = self.get_serializer(page,many=True)
		return self.get_paginated_response(serialiser.data)

	@action(methods=['get'], detail=False)
	def getrate(self, request, format='json'):
		input_id = request.GET.get("id")
		serializer = self.get_serializer(self.get_queryset().get(id = input_id))
		return Response(serializer.data, status=status.HTTP_200_OK)

	@action(methods=['get'], detail=False)
	def rates(self, request):
		product_rates = self.model.objects.values('product').annotate(
			count=Coalesce(Count('product'),0),
			avg=Avg('rate')).order_by("product")
		return Response(product_rates)

	@action(methods=['get'], detail=False)
	def getrate(self, request):
		product = request.GET["product"]
		product_rate = self.model.objects.values('product').annotate(avg_rate=
			Avg('rate')).filter(product=product)
		return Response(product_rate)


	 		



