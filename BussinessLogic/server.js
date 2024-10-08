const express = require('express');
const http = require('http');
const mqtt = require('mqtt');
const cors = require('cors');
const connectDB = require('./config/db')

const sensors = require('./routes/sensor')

require("dotenv").config({ path: "./config/.env" });

//Connect to database
connectDB();

// Create an Express app
const app = express();
const server = http.createServer(app);
const io = require('socket.io')(server, {cors: {origin: "*"}});


// Use CORS middleware allow every request to the server
app.use(cors());

// Body Parser
app.use(express.json())

app.use('/api/v1/sensors', sensors)

// MQTT client setup
const mqttClient = mqtt.connect('mqtt://172.20.10.5'); // Replace with your MQTT broker URL
const topic = 'realtime/data'; // Replace with your topic
const topic2 = 'ml/data';

// MQTT subscription
mqttClient.on('connect', () => {
  console.log('Connected to MQTT broker');
  mqttClient.subscribe(topic, (err) => {
    if (!err) {
      console.log(`Subscribed to topic: ${topic}`);
    }
  });
  mqttClient.subscribe(topic2, (err) => {
    if (!err) {
      console.log(`Subscribed to topic: ${topic2}`);
    }
  });
});

// Handling incoming MQTT messages
mqttClient.on('message', (topic, message) => {
  const dataPoint = message.toString();
  console.log('Received message:', dataPoint);

  // Emit the data to the client through Socket.io
  io.emit('newData', dataPoint);
});

app.get('/', (req, res) => {
    console.log('GET /');
});

// Start the server
server.listen(6996, () => {
  console.log('Server running on http://localhost:6996');
});
