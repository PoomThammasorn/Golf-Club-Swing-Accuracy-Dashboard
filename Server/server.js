require("dotenv").config({ path: "./configs/.env" });

const { startSubscriber } = require("./services/subscriber");

startSubscriber();
