const express = require("express");

const app = express();
const cors = require("cors");

// Load env vars
require("dotenv").config({ path: "configs/.env" });

// Enable CORS
app.use(cors());

// Body parser
app.use(express.json());

app.get("/", (req, res) => {
	res.status(200).json({ success: true, data: "server is running" });
});

const mqtt = require("mqtt");
const client = mqtt.connect(process.env.MQTT_URL);

client.on("connect", () => {
	console.log("Connected to MQTT broker");
	client.subscribe(process.env.MQTT_TOPIC, (err) => {
		if (!err) {
			console.log(`Subscribed to topic: ${process.env.MQTT_TOPIC}`);
		}
	});
});

client.on("message", (topic, message) => {
	console.log(`Received message: ${message.toString()} on topic: ${topic}`);
});

// Port
const PORT = process.env.PORT || 8000;

const server = app.listen(
	PORT,
	console.log(`Server running in ${process.env.NODE_ENV} mode on port ${PORT}`)
);

// Handle unhandled promise rejections
process.on("unhandledRejection", (err, promise) => {
	console.log(`Error: ${err.message}`);
	// Close server & exit process
	server.close(() => process.exit(1));
});
