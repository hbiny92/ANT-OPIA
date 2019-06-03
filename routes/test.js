const express = require('express');
const router = express.Router();


// use ejs and send css,image ...
router.get('/', function(req, res) {
    res.render('test')

});

router.post('/',function (req, res) {
    //send back something..

});


module.exports = router;
