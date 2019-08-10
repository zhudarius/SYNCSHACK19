var express = require("express");
var router = express.Router();
const Processed = require('../models/processed');



router.get('/', function (req, res) {
    res.render('index');
});

router.get('/get_test_data', (req, res) => {
    Processed.find({})
        .exec()
        .then(obj => {
            res.status(200).send(obj);
            // console.log(obj)
        })
        .catch(err => {
            console.log(err);
        })
})



module.exports = router;













Processed.create({ data: { "testKey": new Date() } })
    .then(() => {
        console.log("Created test data.");
    })
    .catch(err => {
        console.log(err);
    })