Installation
************

django-wsync depends on `Django Channels <https://channels.readthedocs.io/en/latest/>`_ and `Django REST framework <http://www.django-rest-framework.org/>`_. These will automatically get installed as Python dependencies, but you will have to manually configure Channels in your Django settings.

Python
======

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

That's it! You should now be able to run ``./manage.py runserver`` as usual, and a WebSocket should be available at ``/wsync/``.

.. note::

	Please note that installing Django Channels will replace the default Django development server with `Daphne <https://github.com/django/daphne>`_, which is capable of handling WebSockets and HTTP/2.


JavaScript
==========

On the JavaScript side of things, all you need to do is load ``wsync.js`` and initialize it. You can then find your serialized Model objects in ``wsync.store.ModelName``:

.. code-block:: html

	<script src="{% static 'wsync.js' %}"></script>
	<script>
		wsync.connect(() => {
			console.log('Webspaces: ', wsync.store.Webspace)
		})
	</script>

The JavaScript library will take care of the nitty-gritty details like WebSocket handling and reconnections.
