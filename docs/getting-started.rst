.. _getting-started:

Getting started
***************

Stream your first model
=======================

First, we need to write a serializer for your model. In our example, the model is called ``Webspace``. You can put your serializers in any file in your app directory, but it's convention to use `serializers.py`::

	from rest_framework.serializers import ModelSerializer
	from .models import Webspace

	class WebspaceSerializer(ModelSerializer):
		class Meta:
			model = Webspace
			fields = ('id', 'host')

These serializers come from Django Rest Framework and don't have any modifications. You should be able to use most of DRF's serialization functionality without adjustments. If you already have existing serializers for a REST API or similar, you should be able to reuse them.

Next, add the ``@stream`` decorator to let django-wsync know about the serializer::

	from rest_framework.serializers import ModelSerializer
	from .models import Webspace
	from wsync import stream

	@stream
	class WebspaceSerializer(serializers.ModelSerializer):
		class Meta:
			model = Webspace
			fields = ('id', 'host')
