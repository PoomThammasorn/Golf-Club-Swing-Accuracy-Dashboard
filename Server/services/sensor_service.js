// sensor_service.js

class SensorService {
	constructor(client, publish_topic, threshold = 2, club_length = 0.85) {
		this.buffer = [];
		this.threshold = threshold; // Impact detection threshold in m/s
		this.club_length = club_length; // Club length in meters
		this.client = client;
		this.publish_topic = publish_topic; // Topic to publish impact data
	}

	addData(gyZ) {
		const timestamp = Date.now();
		gyZ *= Math.PI / 180; // Convert degrees to radians
		this.buffer.push({ timestamp, z: gyZ });

		if (this.buffer.length > 3) {
			this.checkImpact();
		}

		if (this.buffer.length > 10) {
			this.buffer.shift();
		}
	}

	checkImpact() {
		const l = this.buffer[this.buffer.length - 3].z;
		const m = this.buffer[this.buffer.length - 2].z;
		const r = this.buffer[this.buffer.length - 1].z;

		if (m > l && m > r) {
			const velocity = m * this.club_length;
			if (velocity > this.threshold) {
				console.log("Impact detected with velocity:", velocity, "m/s");
				const payload = {
					timestamp: this.buffer[this.buffer.length - 2].timestamp,
					velocity: velocity,
				};
				this.client.publish(
					this.publish_topic,
					JSON.stringify(payload),
					(err) => {
						if (err) {
							console.error("Failed to publish data to webhook:", err);
						} else {
							console.log(
								`Published data to ${this.client.options.host} on publish_topic: ${this.publish_topic}`
							);
						}
					}
				);
				this.clearBuffer();
			}
		}
	}

	clearBuffer() {
		this.buffer = [];
	}

	setThreshold(newThreshold) {
		this.threshold = newThreshold;
	}

	setClubLength(newClubLength) {
		this.club_length = newClubLength;
	}
}

module.exports = SensorService;
