.. _getting-started:

Getting started
===============

django-wsync depends on `Django Channels <https://channels.readthedocs.io/en/latest/>`_ and `Django REST framework <http://www.django-rest-framework.org/>`_. These will be automatically installed as Python dependencies, but you will have to manually include them in your Django settings.

Installation
------------

Install django-wsync from PyPI using your package manager of choice::

	pipenv install django-wsync
	pip install django-wsync

In your Django settings.py, add django-wsync and Django Channels to the installed apps::

	INSTALLED_APPS = [
		[…]
		'channels',
		'wsync',
	]


and also configure the ASGI application for Channels::

	ASGI_APPLICATION = 'wsync.routing.application'


Stream some models
------------------

Next, we need to write a serializer for your model. In our example, the model is called ``Webspace``. You can put your serializers in any file in your app directory, but it's convention to use `serializers.py`::

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

That's it. Next time you start Django using ``./manage.py runserver`` or similar, you should be able to connect to a WebSocket at ``/wsync/``.

JavaScript
----------

On the JavaScript side of things, all you need to do is load ``wsync.js`` and initialize it. You can then find your serialized Model objects in ``wsync.store.ModelName``:

.. code-block:: html

	<script src="{% static 'wsync.js' %}"></script>
	<script>
		wsync.connect(() => {
			console.log('Webspaces: ', wsync.store.Webspace)
		})
	</script>

The JavaScript library will take care of the nitty-gritty details like WebSocket handling and reconnections.
