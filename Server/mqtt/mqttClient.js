const mqtt = require("mqtt");

const connectToMQTT = (url, topic, messageHandler) => {
	const client = mqtt.connect(url);

	client.on("connect", () => {
		console.log("Connected to MQTT broker");
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
