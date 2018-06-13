Welcome to django-wsync's documentation!
****************************************

django-wsync makes it easy to stream changes in your Django models to JavaScript in real-time::

	class Webspace(models.Model):
		host = models.CharField(max_length=50)

	@stream
	class WebspaceSerializer(ModelSerializer):
		class Meta:
			model = Webspace
			fields = ('host',)

JavaScript:

.. code-block:: js

	>> wsync.connect()
	>> wsync.store.Webspace[0].host
	"beep boop"

Now, whenever an instance of your ``Webspace`` model is modified, the changes will be reflected in ``wsync.store``.

.. warning::

	django-wsync is pre-alpha at best. Use in production environments (if even possible) is highly discouraged and at your own risk.

django-wsync is based on `Django Channels <https://channels.readthedocs.io/en/latest/>`_ and `Django REST framework <http://www.django-rest-framework.org/>`_, and can optionally be integrated with JavaScript state management libraries such as `Vuex <https://vuex.vuejs.org/>`_.

Limitations
===========

Nothing works™.

Contents
========

.. toctree::
   :maxdepth: 2

   installation
   getting-started
   reference



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
