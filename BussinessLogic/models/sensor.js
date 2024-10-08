const mongoose = require('mongoose');

const sensorDataSchema = new mongoose.Schema({
    timestamp: {
        type: Date,
        required: [true, "Please add an timestamp."]
    },
    distanceError:{
        type: Number,
        required: [true,"Please add an distance error."]
    }
});

module.exports = mongoose.model("SensorData", sensorDataSchema);