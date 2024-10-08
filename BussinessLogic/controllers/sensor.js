const SensorData = require('../models/sensor');

//@desc Get all SensorData 
//@route Get /api/v1/sensors
//@acess Public
exports.getSensorsdatas = async (req,res,next) => {
    try{
        const sensordatas = await SensorData.find();
        console.log(sensordatas)
        res.status(200).json({success: true, count: sensordatas.length, data: sensordatas});
    }catch(err){
        console.log(err)
        res.status(400).json({success:false});
    }
    
};

//@desc     Create new datasensor
//@route    POST /api/v1/sensor
//@access   Public
exports.createSensorsdata = async (req, res, next) => {
    // console.log(req.body)
    const sensordatas = await SensorData.create(req.body)
    res.status(201).json({success: true, data: sensordatas})
}

//@desc     Delete all datasensor
//@route    DELETE /api/v1/sensor
//@access   Public
exports.deleteAllSensorsdata = async (req, res, next) => {
    // console.log(req.body)
    await SensorData.deleteMany({});
    res.status(200).json({success: true})
}