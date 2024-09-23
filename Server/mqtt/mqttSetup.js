const mqtt = require("mqtt");

const connectToMQTT = (url, port, topic, messageHandler) => {
	console.log(`Connecting to MQTT broker at: ${url}:${port}`);
	const uri = `mqtt://${url}:${port}`;
	const client = mqtt.connect(uri);
	client.on("connect", () => {
		console.log(`Connected to MQTT broker at: ${uri}`);
		client.subscribe(topic, (err) => {
			if (!err) {
				console.log(`Subscribed to topic: ${topic}`);
			} else {
				console.log(`Failed to subscribe to topic: ${topic}`);
			}
		});
	});

	client.on("message", messageHandler);

	return client;
};

module.exports = { connectToMQTT };
