// subscriber.js

const SensorService = require("../services/sensor_service");
const mqtt = require("mqtt");

const client = mqtt.connect("mqtt://localhost");
const sensorService = new SensorService(client);

const subscribeToTopics = (topics) => {
	topics.forEach((topic) => {
		client.subscribe(topic, (err) => {
			if (!err) {
				console.log(`Subscribed to topic: ${topic}`);
			} else {
				console.error(`Failed to subscribe to topic: ${topic}`, err);
			}
		});
	});
};

client.on("connect", () => {
	console.log("Connected to MQTT broker");
	subscribeToTopics(["sensor/data", "camera/video"]);
});

client.on("message", (topic, message) => {
	if (topic === "sensor/data") {
		try {
			message = JSON.parse(message);
			sensorService.addData(message.gyroscope.z);
		} catch (err) {
			console.error("Failed to parse sensor data:", err);
		}
	} else if (topic === "camera/video") {
		console.log("Received video frame");
		// Do later
	}
});

client.on("error", (error) => {
	console.error(`Error: ${error}`);
});

client.on("offline", () => {
	console.log("Client is offline");
});

const shutdown = () => {
	client.end(() => {
		console.log("Disconnected from MQTT broker");
		process.exit(0);
	});
};

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
