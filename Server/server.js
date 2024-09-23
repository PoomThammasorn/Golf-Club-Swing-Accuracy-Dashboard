const express = require("express");
const cors = require("cors");
const { connectToMQTT } = require("./mqtt/mqttSetup");
const { mqttMessageHandler } = require("./mqtt/mqttMessageHandler");
const ml = require("./routes/ml");

require("dotenv").config({ path: "configs/.env" });

const app = express();
app.use(cors());
app.use(express.json());

// Use the health routes
app.get("/", (req, res) => {
	res.status(200).json({ success: true, data: "server is running" });
});

// Use the ML routes
app.use("/api/ml", ml);

// Connect to MQTT broker
connectToMQTT(
	process.env.MQTT_URL || "localhost",
	process.env.MQTT_PORT || 1883,
	process.env.MQTT_SENSORS_TOPIC || "sensors/data",
	mqttMessageHandler
);

// Start server
const PORT = process.env.PORT || 8000;
const server = app.listen(PORT, () => {
	console.log(`Server running in ${process.env.NODE_ENV} mode on port ${PORT}`);
});

process.on("unhandledRejection", (err) => {
	console.log(`Error: ${err.message}`);
	server.close(() => process.exit(1));
});
