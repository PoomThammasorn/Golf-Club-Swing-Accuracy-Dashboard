const express = require("express");
const router = express.Router();
const { sendWebhookML, receiveWebhookML } = require("../controllers/ml");

router.post("/request/:task_id", sendWebhookML);

router.post("/result", receiveWebhookML);

module.exports = router;
