from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.conf import settings

sync_models = {}


class WSyncConsumer(JsonWebsocketConsumer):
	def reply(self, msg_id, data=None, error=None):
		"""Simple wrapper to send a JSON reply in the correct format."""

		self.send_json({'id': msg_id, 'error': error, 'data': data})

	def stream(self, models):
		data = dict()
		for model in models:
			if model not in sync_models:
				continue

			objects = model.objects.all()
			serializer = sync_models[model]['serializer']
			name = sync_models[model]['name']
			data[name] = serializer(objects, many=True).data

		self.reply('stream', data=data)

	def stream_callback(self, sender, **kwargs):
		print('Stream callback for {}'.format(sender))
		self.stream([sender])

	def start_sync(self):
		"""Starts synchronization of models and sends initial stream to client."""

		for model in sync_models.keys():
			post_save.connect(self.stream_callback, sender=model, weak=False)
			post_delete.connect(self.stream_callback, sender=model, weak=False)

		self.stream(sync_models.keys())

	def connect(self):
		"""Handles new client connections."""

		self.accept()
		self.start_sync()

	def disconnect(self, close_code):
		"""Handles client disconnects and removes all Django signals we have registered."""

		for model in sync_models.keys():
			post_save.disconnect(self.stream_callback, sender=model)
			post_delete.disconnect(self.stream_callback, sender=model)

	def edit(self, msg_id, data):
		print('Editing: {}'.format(data))

		serializer = NodeSerializer(data=data['nodes'])

		if not serializer.is_valid():
			self.reply(msd_id, error='Invalid input')

		serializer.save()
		self.reply(msg_id)

	def delete(self, msg_id, data):
		print('Deleting: {}'.format(data))
		Node.objects.get(id=data['nodes']).delete()
		self.reply(msg_id)

	def receive_json(self, message):
		if not all(('cmd' in message, 'id' in message)):
			return

		cmd = message['cmd']
		msg_id = message['id']

		commands = {
			'edit': self.edit,
			'delete': self.delete,
		}

		if cmd not in commands:
			print('invalid command', cmd)
			return self.reply(msg_id, error='Invalid command')

		return commands[cmd](msg_id, message.get('data'))
