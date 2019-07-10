const express = require('express');
const multer = require('multer');
const spawn = require('child_process').spawn

var upload = multer({
    storage: multer.diskStorage({
        destination: './public/images',
        filename: (req, file, next) => {
            next(null, file.originalname);
        }
    })
});

var app = express();

app.use(express.static('./public'));

app.listen(process.env.PORT || 80, () => {
    console.log('Start on 80');
});

app.get('/', (req, res) => {
    res.render('index.ejs');
});

app.post('/', upload.single('image'), (req, res) => {
    var dummy = spawn('C:/Users/Francois/.conda/envs/tfCPU/python.exe', ['scripts/result.py', req.file.path]);

    dummy.stdout.on('data', (data) => {
        var result = data.toString()
    
        if (result == 'Dog' || result == 'Cat') {
            res.render('index.ejs', {
                image: 'images/' + req.file.filename,
                result: result
            });
        }
    });
});