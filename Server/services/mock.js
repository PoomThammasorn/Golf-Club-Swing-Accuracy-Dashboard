// mock.js

class Mock {
	constructor(client) {
		this.client = client;
	}

	auto_publish() {
		setInterval(() => {
			const payload = {
				timestamp: Date.now(),
				velocity: Math.random() * 10,
			};
			this.client.publish("realtime/data", JSON.stringify(payload), (err) => {
				if (!err) {
					console.log(
						`Published sensor data at timestamp: ${payload.timestamp} velocity: ${payload.velocity}`
					);
				} else {
					console.error("Failed to publish sensor data", err);
				}
			});
		}, 1000);
	}
}

module.exports = Mock;
