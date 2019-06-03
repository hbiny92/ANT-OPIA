const express = require('express');
const router = express.Router();


// use ejs and send css,image ...
router.get('/', function(req, res) {
    res.render('index')

});

router.post('/',function (req, res) {
    //send back something..
    res.render('index')
});


module.exports = router;
