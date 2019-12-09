
# Django Imports
from rest_framework import serializers


# app level Imports
from .models import (
					rating,
					)

class RatingAddSerializer(serializers.ModelSerializer):
	created_at = serializers.DateTimeField(required=False)

	class Meta:
		model = rating
		fields = '__all__'

	def validate(self,data):		
		return data


	def create(self, validated_data):
		return rating.objects.create(**validated_data)


class ListRatingSerializer(serializers.ModelSerializer):
	created_at = serializers.DateTimeField(required=False)

	class Meta:
		model = rating
		fields = '__all__'