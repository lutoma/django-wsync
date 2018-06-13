django-wsync
============

django-wsync streams changes in your Django models to your frontend using WebSockets. It is based on `Django Channels <https://channels.readthedocs.io/en/latest/>`_ and uses `Django REST framework <http://www.django-rest-framework.org/>`_'s serializers. It can also be integrated with JavaScript state management libraries such as `Vuex <https://vuex.vuejs.org/>`_.

`📖 Documentation, installation and getting started instructions_ <https://django-wsync.lutoma.org>`_

Please note that this project is released with a `Contributor Code of Conduct <https://github.com/lutoma/django-wsync/blob/master/CODE_OF_CONDUCT.md>`_. By participating in this project you agree to abide by its terms.


Example
-------

Note that this is missing imports. For a full example check `Getting Started <https://django-wsync.lutoma.org/getting-started.html>`_

.. code-block:: python

	class Webspace(models.Model):
		host = models.CharField(max_length=50)

	@stream
	class WebspaceSerializer(ModelSerializer):
		class Meta:
			model = Webspace
			fields = ('host',)

.. code-block:: js

	>> wsync.connect()
	>> wsync.store.Webspace[0].host
	"beep boop"

Now, whenever an instance of your ``Webspace`` model is modified, the changes will be reflected in ``wsync.store``.

