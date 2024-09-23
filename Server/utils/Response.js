const SuccessResponse = (message = null, data = null) => {
	return {
		success: true,
		data,
		message,
	};
};

const ErrorResponse = (message = "Internal Server Error") => {
	return {
		success: false,
		message,
	};
};

module.exports = { SuccessResponse, ErrorResponse };
