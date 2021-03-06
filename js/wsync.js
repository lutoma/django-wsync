window.wsync = {
	socket: null,
	listeners: {},
	store: {},
	uuid: 0,
	reconnect_attempt: 0,

	cmd(cmd, data = null) {
		let id = this.uuid++
		let promise = new Promise((resolve, reject) => {
			this.listeners[id] = (message) => {
				delete this.listeners[id]

				if(message.error) {
					reject(message.error)
				} else {
					resolve(message.data)
				}
			}
		})

		let message = JSON.stringify({cmd, data, id})
		this.socket.send(message)
		return promise
	},

	receive(event) {
		let message = JSON.parse(event.data)
		console.log('wsync: In:', event.data)

		if(message.id === 'stream') {
			for(let key of Object.keys(message.data)) {
				this.store[key] = message.data[key].reduce((list, obj) => {
					list[obj.id || obj.name] = obj
					return list
				}, {})
			}
		}

		if(message.id in this.listeners) {
			return this.listeners[message.id](message)
		}
	},

	connect() {
		return new Promise((resolve, reject) => {
			// Reconnections
			if(this.socket) {
				this.socket.close()
			}

			this.socket = new WebSocket("ws://127.0.0.1:8000/wsync/")
			this.socket.addEventListener('open', (event) => {
				console.debug('wsync: Connection established')
				resolve(event)
			})

			this.socket.addEventListener('message', (event) => this.receive(event))
			this.socket.addEventListener('close', (event) => this.close(event))
		})
	},

	close(event) {
		console.debug('wsync: Connection closed')

		// Try reconnecting if we haven't already
		if(this.reconnect_attempt++ < 2) {
			console.debug('wsync: Attempting to reconnect')
			this.connect()
		} else {
			console.debug('wsync: Connection lost')
		}
	},
}
