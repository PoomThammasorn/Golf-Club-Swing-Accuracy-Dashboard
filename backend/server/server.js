// server.js

const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post('/webhook', (req, res) => {
    console.log('Received a webhook event:', req.body);
    res.status(200);
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
