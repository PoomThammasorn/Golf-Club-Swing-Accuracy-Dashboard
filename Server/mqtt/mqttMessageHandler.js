let data = [];
let lastLogTime = Date.now();
const MAX_DATA_POINTS = 1000; // Limit the number of data points for averaging
const LOG_COOLDOWN = 1000; // Log the average every second

const mqttMessageHandler = async (topic, message) => {
	try {
		const dataPoint = JSON.parse(message);
		if (dataPoint.data !== undefined) {
			// Store the data point
			data.push(dataPoint.data);

			// If we exceed MAX_DATA_POINTS, remove the oldest entry
			if (data.length > MAX_DATA_POINTS) {
				data.shift();
			}

			// Calculate average
			const averageAccelerometer_x =
				data.reduce((acc, val) => acc + val.gyroscope.x, 0) / data.length;
			const averageAccelerometer_y =
				data.reduce((acc, val) => acc + val.gyroscope.y, 0) / data.length;
			const averageAccelerometer_z =
				data.reduce((acc, val) => acc + val.gyroscope.z, 0) / data.length;

			const averageGyroscope_x =
				data.reduce((acc, val) => acc + val.accelerometer.x, 0) / data.length;
			const averageGyroscope_y =
				data.reduce((acc, val) => acc + val.accelerometer.y, 0) / data.length;
			const averageGyroscope_z =
				data.reduce((acc, val) => acc + val.accelerometer.z, 0) / data.length;

			if (Date.now() - lastLogTime > LOG_COOLDOWN) {
				lastLogTime = Date.now();
				// Log the average
				console.log(`Average sensor data at ${new Date().toISOString()}`);
				console.log(
					`Average accelerometer: ${averageAccelerometer_x}, ${averageAccelerometer_y}, ${averageAccelerometer_z}`
				);
				console.log(
					`Average gyroscope: ${averageGyroscope_x}, ${averageGyroscope_y}, ${averageGyroscope_z}\n`
				);
			}
		}
	} catch (error) {
		console.error(`Error processing message: ${error.message}`);
	}
};

module.exports = { mqttMessageHandler };
