const express = require("express");
const cors = require("cors");
const ml = require("./routes/ml");

require("dotenv").config({ path: "./configs/.env" });

const { startSubscriber } = require("./services/subscriber");

const app = express();
app.use(cors());
app.use(express.json());

// Use the health routes
app.get("/", (req, res) => {
	res.status(200).json({ success: true, data: "server is running" });
});

// Use the ML routes
app.use("/webhook/ml", ml);

startSubscriber();

// Start server
const PORT = process.env.PORT || 8000;
const server = app.listen(PORT, () => {
	console.log(`Server running on port ${PORT}`);
});

process.on("unhandledRejection", (err) => {
	console.log(`Error: ${err.message}`);
	server.close(() => process.exit(1));
});
