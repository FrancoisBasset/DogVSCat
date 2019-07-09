const express = require('express');
const multer = require('multer');
const spawn = require('child_process').spawn

var upload = multer({
    storage: multer.diskStorage({
        destination: './images',
        filename: (req, file, next) => {
            next(null, file.originalname);
        }
    })
});

var app = express();

app.use(express.static('./'));

app.listen(80, () => {
    console.log('Start on 80');
});

app.get('/', (req, res) => {
    res.render('index.ejs');
});

app.post('/', upload.single('image'), (req, res) => {
    var dummy = spawn('C:/Users/Francois/.conda/envs/tfCPU/python.exe', ['result.py', req.file.path]);

    dummy.stdout.on('data', (data) => {
        var result = data.toString()
    
        if (result == 'Dog' || result == 'Cat') {
            res.render('index.ejs', {
                image: req.file.path,
                result: result
            });
        }
    });
});