# python imports
import uuid

# django/rest_framwork imports
from django.db import models
from django.core.validators import (
	MaxValueValidator,
	MinValueValidator
	)

# project level imports
from libs.models import TimeStampedModel

# third party imports
# from model_utils import Choices
# from jsonfield import JSONField

class rating(TimeStampedModel):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	rate = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
	feedback = models.TextField()
	product = models.CharField(max_length=50)
	subscription_id = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)

	def __str__(self):
        return str(self.product)