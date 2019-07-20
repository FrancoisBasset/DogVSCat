const express = require('express');
const spawn = require('child_process').spawn
const fs = require('fs');


var app = express();

app.use(express.static('./public'));

app.listen(process.env.PORT || 80, () => {
    console.log('Start on 80');
});

app.get('/', (req, res) => {
    var images = fs.readdirSync('./public/images');
    images.splice(0, 1);

    var cats = [];
    var dogs = [];
    
    for (var image of images) {
        var dummy = spawn('C:/Users/Francois/.conda/envs/tfCPU/python.exe', ['scripts/result.py', 'public/images/' + image]);

        dummy.stdout.on('data', (data) => {
            var result = data.toString()
        
            if (result.includes('dog') || result.includes('cat')) {
                var type = result.split(',')[0];
                var image = result.split(',')[1];
                image = image.split('/')[1] + '/' + image.split('/')[2];

                if (type == 'dog') {
                    dogs.push(image);
                }
                if (type == 'cat') {
                    cats.push(image);
                }
                
                if (dogs.length + cats.length == images.length) {
                    res.render('index.ejs', {
                        dogs: dogs,
                        cats: cats
                    });

                    return;
                }
            }
        });
    }
});