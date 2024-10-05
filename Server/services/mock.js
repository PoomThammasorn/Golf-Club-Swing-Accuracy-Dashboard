// mock.js
const SensorData = require('../models/sensor');

class Mock {
	constructor(client) {
		this.client = client;
	}

	auto_publish() {
		setInterval(async() => {
			const payload = {
				timestamp: Date.now(),
				velocity: Math.random() * 10,
			};
			const sensorData = new SensorData(payload);
			try{
				await sensorData.save();
				console.log(`Data saved to MongoDB: ${JSON.stringify(payload)}`);
				this.client.publish("realtime/data", JSON.stringify(payload), (err) => {
					if (!err) {
						console.log(
							`Published sensor data at timestamp: ${payload.timestamp} velocity: ${payload.velocity}`
						);
					} else {
						console.error("Failed to publish sensor data", err);
					}
			});
		} catch(err){
			console.error("Error saving data to MongoDB:", err);
		}
		}, 1000);
	}
}

module.exports = Mock;
