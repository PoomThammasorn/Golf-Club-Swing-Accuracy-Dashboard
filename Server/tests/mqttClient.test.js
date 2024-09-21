// Import the function to be tested
const { connectToMQTT } = require("../mqtt/mqttClient");
const mqtt = require("mqtt");

// Mock the MQTT library
jest.mock("mqtt");

describe("connectToMQTT", () => {
	let mockClient;

	beforeEach(() => {
		// Reset any previous mock calls
		jest.clearAllMocks();

		// Mock MQTT client methods
		mockClient = {
			on: jest.fn(),
			subscribe: jest.fn((topic, callback) => callback(null)),
		};

		// Mock mqtt.connect to return the mocked client
		mqtt.connect.mockReturnValue(mockClient);
	});

	it("should connect to the MQTT broker", () => {
		const url = "test-url";
		const port = 1883;
		const topic = "test/topic";
		const messageHandler = jest.fn();

		// Call the function
		connectToMQTT(url, port, topic, messageHandler);

		// Assert mqtt.connect was called with the correct URL and port
		expect(mqtt.connect).toHaveBeenCalledWith(`mqtt://${url}:${port}`);
	});

	it("should subscribe to the topic after connecting", () => {
		const url = "test-url";
		const port = 1883;
		const topic = "test/topic";
		const messageHandler = jest.fn();

		// Call the function
		connectToMQTT(url, port, topic, messageHandler);

		// Simulate the 'connect' event
		const connectCallback = mockClient.on.mock.calls.find(
			(call) => call[0] === "connect"
		)[1];
		connectCallback();

		// Assert that subscribe is called with the correct topic
		expect(mockClient.subscribe).toHaveBeenCalledWith(
			topic,
			expect.any(Function)
		);
	});

	it("should handle incoming messages", () => {
		const url = "test-url";
		const port = 1883;
		const topic = "test/topic";
		const messageHandler = jest.fn();

		// Call the function
		connectToMQTT(url, port, topic, messageHandler);

		// Simulate the 'message' event
		const messageCallback = mockClient.on.mock.calls.find(
			(call) => call[0] === "message"
		)[1];
		const mockMessage = Buffer.from("test message");
		messageCallback(topic, mockMessage);

		// Assert the messageHandler is called with the correct parameters
		expect(messageHandler).toHaveBeenCalledWith(topic, mockMessage);
	});
});
