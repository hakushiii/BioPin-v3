const express = require('express');
const fs = require('fs');

const app = express();
const port = 3000;

app.use(express.static('public'));

app.post('/save', express.json(), (req, res) => {
    const data = req.body;
    const filename = 'public/sliderData.json';

    // Read the existing file content
    let existingData = [];
    try {
        existingData = JSON.parse(fs.readFileSync(filename));
    } catch (error) {
        // File doesn't exist or is not valid JSON
    }

    // Append or overwrite data
    existingData.push(data);

    // Write the updated content back to the file
    fs.writeFileSync(filename, JSON.stringify(existingData, null, 2));

    res.sendStatus(200);
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
s