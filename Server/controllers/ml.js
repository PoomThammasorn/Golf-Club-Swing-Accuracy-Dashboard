const axios = require("axios");
const { SuccessResponse, ErrorResponse } = require("../utils/Response");

exports.sendWebhookML = async (req, res) => {
	try {
		const { task_id } = req.params;
		if (!task_id) {
			return res.status(400).json(ErrorResponse("Invalid task_id"));
		}

		const mlServiceUrl =
			process.env.ML_SERVICE_URL || "http://localhost:9000/api/ml";
		response = await axios.post(`${mlServiceUrl}/data/${task_id}`);

		res
			.status(200)
			.json(SuccessResponse("Request sent to ML service successfully"));
	} catch (error) {
		console.error("Error sending request to ML service:", error);
		res.status(500).json(ErrorResponse("Internal Server Error"));
	}
};

exports.receiveWebhookML = async (req, res) => {
	try {
		const result = req.body;

		if (!result) {
			return res.status(400).json(ErrorResponse("Invalid result"));
		}

		res
			.status(200)
			.json(SuccessResponse(`Received result for task ${result.task_id}`));
		console.log(
			`Received result for task ${
				result.task_id
			} with payload: ${JSON.stringify(result.data)}`
		);
	} catch (error) {
		console.error("Error processing ML result:", error);
		res.status(500).json(ErrorResponse("Internal Server Error"));
	}
};
