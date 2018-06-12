default_app_config = 'wsync.apps.WsyncConfig'


class stream:
	def __init__(self, serializer):
		from .consumers import sync_models

		model = serializer.Meta.model
		sync_models[model] = {
			'name': model.__name__,
			'serializer': serializer,
		}
