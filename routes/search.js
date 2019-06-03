const express = require('express');
const router = express.Router();


// use ejs and send css,image ...
router.get('/', function(req, res) {
    res.render('search')

});

router.post('/',function (req, res) {
    //send back something..

});


module.exports = router;
