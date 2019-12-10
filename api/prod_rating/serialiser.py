
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

	class Meta:
		model = rating
		fields = '__all__'

class RatingUpdateSerializer(serializers.ModelSerializer):
	rate = serializers.IntegerField(required=False)
	feedback = serializers.CharField(required=False)

	class Meta:
		model = rating
		fields = ('id','rate','feedback')

	def validate(self,data):		
		return data


	def update(self, instance,validated_data):
		instance.rate = validated_data.get('rate',instance.rate)
		instance.feedback = validated_data.get('feedback',instance.feedback)
		instance.save()
		return instance