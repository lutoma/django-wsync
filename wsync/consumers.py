from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.conf import settings
import jwt

sync_models = {}


class WSyncConsumer(JsonWebsocketConsumer):
	user = None

	def reply(self, msg_id, data=None, error=None):
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

	def connect(self):
		self.accept()
		self.start_sync()

	def disconnect(self, close_code):
		for model in sync_models.keys():
			post_save.disconnect(self.stream_callback, sender=model)
			post_delete.disconnect(self.stream_callback, sender=model)

	def start_sync(self):
		for model in sync_models.keys():
			post_save.connect(self.stream_callback, sender=model, weak=False)
			post_delete.connect(self.stream_callback, sender=model, weak=False)

		self.stream(sync_models.keys())

	def login(self, msg_id, data):
		'''
		Login to obtain a new token
		'''
		if not data or not ('username' in data and 'password' in data):
			self.error(msg_id, 'Missing fields')
			return

		print('Logging in as {}'.format(data['username']))
		user = authenticate(username=data['username'], password=data['password'])

		if not user:
			return self.reply(msg_id, error='Invalid login credentials')

		self.user = user
		payload = {
			'uid': user.id,
		}

		token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
		self.reply(msg_id, {'token': token})
		self.start_sync()

	def auth(self, msg_id, data):
		'''
		Re-authenticate with a previously obtained token
		'''

		if not data or 'token' not in data:
			return self.reply(msg_id, error='Missing fields')

		token_data = jwt.decode(data['token'].encode('utf-8'), settings.SECRET_KEY, algorithm='HS256')

		if 'uid' not in token_data:
			return self.reply(msg_id, error='Invalid token')

		self.user = User.objects.get(id=token_data['uid'])
		self.reply(msg_id)
		self.start_sync()

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
			'login': self.login,
			'auth': self.auth,
			'edit': self.edit,
			'delete': self.delete,
		}

		if not self.user and cmd not in ('login', 'auth'):
			return self.reply(msg_id, error='Not authenticated')

		if cmd not in commands:
			print('invalid command', cmd)
			return self.reply(msg_id, error='Invalid command')

		return commands[cmd](msg_id, message.get('data'))
