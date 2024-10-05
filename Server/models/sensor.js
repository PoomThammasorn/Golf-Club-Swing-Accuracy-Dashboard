const mongoose = require('mongoose');

const sensorDataSchema = new mongoose.Schema({
    timestamp: {
        type: Date,
        required: [true,"Please add an timestamp"]
    },
    velocity:{
        type: Number,
        required: [true,"Please add an velocity"]
    }
});

module.exports = mongoose.model("SensorData",sensorDataSchema);