const express = require('express')
const {getSensorsdatas,createSensorsdata, deleteAllSensorsdata} = require('../controllers/sensor')
const router = express.Router()

router.route('/').get(getSensorsdatas).post(createSensorsdata).delete(deleteAllSensorsdata)

module.exports = router