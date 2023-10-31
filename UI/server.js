const express = require('express');
const fs = require('fs');
const app = express();
const path = require('path');
const port = 3000;

app.use(express.json());

app.use(express.static(__dirname));
app.use(express.static(path.join(__dirname, 'public')));

app.get('/getData2', (req, res) => {
    try {
        const rawData = fs.readFileSync('data2.json');
        const data2 = JSON.parse(rawData);
        res.json(data2);
    } catch (error) {
        console.error('Error reading data from file:', error.message);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.post('/saveData', (req, res) => {
    const { direction, combinedValues } = req.body;

    let data = {};
    try {
        const rawData = fs.readFileSync('data.json');
        data = JSON.parse(rawData);
    } catch (error) {
        console.error('Error reading data from file:', error.message);
    }

    if (direction) {
        data.direction = direction;
    }

    if (combinedValues) {
        data.combinedValues = combinedValues;
    }

    try {
        fs.writeFileSync('data.json', JSON.stringify(data, null, 2));
        console.log('Data saved successfully.');
    } catch (error) {
        console.error('Error writing data to file:', error.message);
    }

    res.json({ message: 'Data saved successfully.' });
});

app.post('/storeCommand', express.json(), (req, res) => {
    const { command } = req.body;
  
    // Store the command in a JSON file
    fs.writeFileSync('command.json', JSON.stringify({ command }));
  
    res.send('Command stored successfully.');
  });
  

//Routes
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, 'public', 'main.html'));
});

app.get('/speed', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'speed.html'));
});

app.get('/eog', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'eog.html'));
});

app.get('/eeg', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'eeg.html'));
});

app.get('/control', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'test2.html'));
});

app.get('/direction', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'direction.html'));
});

app.get('/help', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'help.html'));
});



app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
