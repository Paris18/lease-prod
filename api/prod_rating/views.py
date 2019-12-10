# python imports
import json
from datetime import datetime

# Django Imports
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from django.db.models import Count,Q,Sum,Avg,Max,Min
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
	http_method_names = ['get', 'post', 'put']
	model = rating

	def get_queryset(self,filterdata=None):
		if filterdata:
			return self.model.objects.filter(**filterdata)
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
				return Response({"status":"Successfully rated Product"}, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			raise ParseException(BAD_REQUEST, serializer.errors)


	@action(methods=['get'], detail=False)
	def ratelist(self, request, format='json'):
		try:
			filterdata = self.query_string(request.query_params.dict())
			page = self.paginate_queryset(self.get_queryset())
			serialiser = self.get_serializer(page,many=True)
			return self.get_paginated_response(serialiser.data)
		except:
			raise ParseException(BAD_REQUEST)

	@action(methods=['get'], detail=False)
	def getrate(self, request, format='json'):
		try:
			input_id = request.GET.get("id")
			serializer = self.get_serializer(self.get_queryset().get(id = input_id))
			return Response(serializer.data, status=status.HTTP_200_OK)
		except:
			raise ParseException(BAD_REQUEST)

	@action(methods=['get'], detail=False)
	def rates(self, request):
		try:
			product_rates = self.model.objects.values('product').annotate(avg_rate=
				Avg('rate'),max_rate = Max('rate'),min_rate=Min('rate'),no_of_rates=Count('rate')).order_by("product")
			return Response(product_rates)
		except:
			raise ParseException(BAD_REQUEST)

	@action(methods=['get'], detail=False)
	def product_rate(self, request):
		try:
			product = request.GET["product"]
			product_rate = self.model.objects.values('product').annotate(avg_rate=
				Avg('rate'),max_rate = Max('rate'),min_rate=Min('rate'),no_of_rates=Count('rate')).filter(product=product)
			return Response(product_rate)
		except:
			raise ParseException(BAD_REQUEST)


	 		



