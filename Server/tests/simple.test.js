// tests/server.test.js

const request = require("supertest");
const express = require("express");
const cors = require("cors");
require("dotenv").config({ path: "configs/.env" });

// Initialize the Express app
const app = express();
app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
	res.status(200).json({ success: true, data: "server is running" });
});

// Test suite
describe("GET /", () => {
	it("should return a 200 status and success message", async () => {
		const response = await request(app).get("/");
		expect(response.status).toBe(200);
		expect(response.body).toEqual({
			success: true,
			data: "server is running",
		});
	});
});
