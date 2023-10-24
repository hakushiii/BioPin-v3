const express = require('express');
const fs = require('fs');
const app = express();
const path = require('path');
const port = 3000; // You can change this port if needed

app.use(express.json());

app.post('/saveData', (req, res) => {
    const rangeValue = req.body.rangeValue;

    // Load existing data from JSON file
    let data = [];
    try {
        const rawData = fs.readFileSync('data.json');
        data = JSON.parse(rawData);
    } catch (error) {
        console.error('Error reading data from file:', error.message);
    }

    // Add new data
    data = {
        speed: rangeValue
    };

    // Save data back to JSON file
    try {
        fs.writeFileSync('data.json', JSON.stringify(data, null, 2));
        console.log('Data saved successfully.');
    } catch (error) {
        console.error('Error writing data to file:', error.message);
    }

    res.send('Data saved successfully.');
});

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, 'public', 'main.html'));
});

app.get('/pwm', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'pwm.html'));
});

app.get('/eog', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'eog.html'));
});

app.get('/eeg', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'eeg.html'));
});

app.get('/control', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'control.html'));
});

app.get('/direction', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'direction.html'));
});

app.get('/help', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'about.html'));
});



app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
