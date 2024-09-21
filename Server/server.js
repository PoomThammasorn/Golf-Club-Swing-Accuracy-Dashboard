const express = require("express");
const cors = require("cors");
require("dotenv").config({ path: "configs/.env" });

const { connectToMQTT } = require("./mqtt/mqttClient");
const app = express();
app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
	res.status(200).json({ success: true, data: "server is running" });
});

const mqttMessageHandler = async (topic, message) => {
	const messageStr = message.toString();
	console.log(`Received message: ${messageStr} on topic: ${topic}`);

	// Process the message using business logic
	const processedData = processMessage(messageStr);

	// Send data to BI and save to DB
	sendToBI(processedData);
	await saveToDatabase(processedData);
};

// Connect to MQTT broker
connectToMQTT(process.env.MQTT_URL, process.env.MQTT_TOPIC, mqttMessageHandler);

// Start server
const PORT = process.env.PORT || 8000;
const server = app.listen(PORT, () => {
	console.log(`Server running in ${process.env.NODE_ENV} mode on port ${PORT}`);
});

process.on("unhandledRejection", (err) => {
	console.log(`Error: ${err.message}`);
	server.close(() => process.exit(1));
});
