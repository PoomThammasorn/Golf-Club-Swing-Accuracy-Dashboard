const SensorData = require('../models/sensor');

//@desc Get all SensorData 
//@route Get /api/v1/sensordatas
//@acess Public
exports.getSensorsdata = async (req,res,next) => {
    try{
        const sensordatas = await SensorData.find();
        res.status(200).json({success:true,count:sensordatas.length,data:sensordatas});
    }catch(err){
        res.status(400).json({success:false});
    }
    
};
