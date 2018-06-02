var express = require('express'); //load
var path = require('path');
var bodyParser = require('body-parser');
var AWS = require('aws-sdk');
AWS.config.update({region: 'us-east-2'});


var app = express();
var ddb = new AWS.DynamoDB({apiVersion: '2012-08-10'});

// configure app
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
// use middleware
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(express.static(path.join(__dirname,'bower_components/')));

app.get('/', function(req, res) {
    res.render('index', {
        theme: process.env.THEME || 'default',
        flask_debug: process.env.FLASK_DEBUG || 'false'
    });
});
app.get('/about', function(req, res) {
    res.render('about', {
        theme: process.env.THEME || 'default',
        flask_debug: process.env.FLASK_DEBUG || 'false'
    });
});
app.get('/stateparks', function(req, res) {
    console.log(req.query);
    res.render('stateparks', {
        theme: process.env.THEME || 'default',
        flask_debug: process.env.FLASK_DEBUG || 'false'
    });
});
app.get('/hotsprings', function(req, res) {
    res.render('hotsprings', {
        theme: process.env.THEME || 'default',
        flask_debug: process.env.FLASK_DEBUG || 'false'
    });
});
app.get('/horseback', function(req, res) {
    res.render('horseback', {
        theme: process.env.THEME || 'default',
        flask_debug: process.env.FLASK_DEBUG || 'false'
    });
});
app.get('/winecountry', function(req, res) {
    res.render('winecountry', {
        theme: process.env.THEME || 'default',
        flask_debug: process.env.FLASK_DEBUG || 'false'
    });
});
app.get('/golfcourse', function(req, res) {
    res.render('golfcourse', {
        theme: process.env.THEME || 'default',
        flask_debug: process.env.FLASK_DEBUG || 'false'
    });
});

app.get('/eventInfo', function(req, res) {
    var data = req.query;
    var params = {
      TableName: 'ColoradoFunDevTable',
      Key: {
        'id' : {S: data.id},
      }
    };
    // Call DynamoDB to read the item from the table
    ddb.getItem(params, function(err, data) {
      if (err) {
        console.log("Error", err);
      } else {
        // Find events within 10 miles
        var eventLat = data.Item['lat']['S'];
        var eventLng = data.Item['lng']['S'];
        var latRange = 69.172/10;
        var lngRange = 10/(Math.cos(eventLat*3.1415926/180)*69.172)

        // find events where eventLat+latRange<lat<eventLat+latRange
        //               AND eventLng+lngRange<lng<eventLng+lngRange
        res.render('eventinfo', {
            event: data.Item,
            theme: process.env.THEME || 'default',
            flask_debug: process.env.FLASK_DEBUG || 'false'
        });
      }
    });
});

app.get('/map', function(req, res) {
    var params = {
        TableName: 'ColoradoFunDevTable'
    }
    var Mydata = [];
    ddb.scan(params, function(err, data){
        if(err){
            console.log("error", err);
        } else {
            data.Items.forEach(function(element, index, array) {
                Mydata.push(element);
            });        
        }
        res.render('map', {
            events: Mydata,
            theme: process.env.THEME || 'default',
            flask_debug: process.env.FLASK_DEBUG || 'false' 
        });
    })
});
app.get('/user', function(req, res) {
    res.render('user', {
        theme: process.env.THEME || 'default',
        flask_debug: process.env.FLASK_DEBUG || 'false'
    });
});

var port = process.env.PORT || 3000;


var server = app.listen(port, function () {
    console.log('Server running at http://127.0.0.1:' + port + '/');

});
