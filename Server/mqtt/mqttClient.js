const mqtt = require("mqtt");

const connectToMQTT = (url, port, topic, messageHandler) => {
	const client = mqtt.connect(url, { port });

	client.on("connect", () => {
		console.log(`Connected to MQTT broker at: ${url}`);
		client.subscribe(topic, (err) => {
			if (!err) {
				console.log(`Subscribed to topic: ${topic}`);
			}
		});
	});

	client.on("message", messageHandler);

	return client;
};

module.exports = { connectToMQTT };
