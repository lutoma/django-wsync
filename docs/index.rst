Welcome to django-wsync's documentation!
========================================

django-wsync makes it easy to add real-time updates to your Django/JavaScript project::

	@stream
	class WebspaceSerializer(ModelSerializer):
		class Meta:
			model = Webspace
			fields = ('id', 'host')

JavaScript:

.. code-block:: js

	wsync.connect(() => {
		console.log(wsync.store.Webspace[0])
	})

Voilà. Now, whenever an instance of your ``Webspace`` model is modified, the changes will be reflected in ``wsync.store`` in real-time.

django-wsync is based on `Django Channels <https://channels.readthedocs.io/en/latest/>`_ and `Django REST framework <http://www.django-rest-framework.org/>`_, and can optionally be integrated with JavaScript state management libraries such as `Vuex <https://vuex.vuejs.org/>`_.

See the :ref:`getting-started` page for setup instructions and first steps with django-wsync.

Contents
--------

.. toctree::
   :maxdepth: 2

   tutorial



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
