// subscriber.js

const SensorService = require("../services/sensor_service");
const mqtt = require("mqtt");

const host_url = process.env.MQTT_HOST || "localhost";
const client = mqtt.connect(`mqtt://${host_url}`);
const sensors_topic = process.env.MQTT_SENSORS_TOPIC || "sensor/data";
const publish_topic = process.env.MQTT_FRONTEND_TOPIC || "realtime/data";
const sensorService = new SensorService(client, publish_topic);

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

const shutdown = () => {
	client.end(() => {
		console.log("Disconnected from MQTT broker");
		process.exit(0);
	});
};

const startSubscriber = () => {
	console.log(`Starting MQTT subscriber on host ${host_url}`);
	client.on("connect", () => {
		console.log("Connected to MQTT broker");
		subscribeToTopics([sensors_topic]);
	});

	client.on("message", (topic, message) => {
		if (topic === sensors_topic) {
			try {
				message = JSON.parse(message);
				// console.log(message.accelerometer.x);
				sensorService.addData(message.accelerometer.x);
			} catch (err) {
				console.error("Failed to parse sensor data:", err);
			}
		}
	});

	client.on("error", (error) => {
		console.error(`Error: ${error}`);
	});

	client.on("offline", () => {
		console.log("Client is offline");
	});

	process.on("SIGINT", shutdown);
	process.on("SIGTERM", shutdown);
};

startSubscriber();
module.exports = { startSubscriber };
