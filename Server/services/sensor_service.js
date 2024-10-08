// sensor_service.js
const axios = require("axios");

class SensorService {
	constructor(client, publish_topic, threshold = 8.5) {
		this.top_swing = { timestamp: 0, x: 1e9 };
		this.threshold = threshold; // Impact detection threshold in m/s
		this.client = client;
		this.publish_topic = publish_topic; // Topic to publish impact data
		this.ml_service_url = process.env.ML_SERVICE_URL || "http://localhost:9000";
	}

	calculateVelocity(timestamp, acX) {
		const dt = (timestamp - this.top_swing.timestamp) / 1000;
		return Math.abs(acX - this.top_swing.x) / dt;
	}

	addData(acX) {
		const timestamp = Date.now();
		if (acX < this.top_swing.x) {
			this.top_swing = { timestamp: timestamp, x: acX };
		}
		if (this.top_swing.x < -1 && Math.floor(Math.abs(acX)) === 0) {
			const velocity = this.calculateVelocity(timestamp, acX);
			if (velocity > this.threshold) {
				console.log("Impact detected with velocity:", velocity, "m/s");
				const payload = {
					timestamp: timestamp,
					velocity: velocity,
				};
				// Notify to ML service
				axios
					.post(`${this.ml_service_url}/ml`, { timestamp: timestamp })
					.then((res) => {
						console.log(`Response from ML service: ${res.status}`);
					})
					.catch((error) => {
						console.error("Error calling ML service:");
					});

				// Publish data to frontend
				this.client.publish(
					this.publish_topic,
					JSON.stringify(payload),
					(err) => {
						if (err) {
							console.error("Failed to publish data to webhook:", err);
						} else {
							console.log(
								`Published data to ${this.client.options.host} on publish_topic: ${this.publish_topic} at ${timestamp}`
							);
						}
					}
				);
				this.clearTopSwing();
			}
		}
	}

	clearTopSwing() {
		this.top_swing = { timestamp: 0, x: 1e9 };
	}

	setThreshold(newThreshold) {
		this.threshold = newThreshold;
	}

	setClubLength(newClubLength) {
		this.club_length = newClubLength;
	}
}

module.exports = SensorService;
