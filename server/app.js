const express = require('express');
const app = express();
const mongoose = require('mongoose');
const bodyParser = require("body-parser");


let PORT = 80;

app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({ extended: true }));


var indexRoutes = require("./routes/index");
app.use(indexRoutes);

app.use(express.static('assets'))


// Connect to the DB.
mongoose.connect('mongodb://localhost/SYNCSHACK2019')
    .then(() => {
        console.log("Successfully connected to MongoDB.");
    })
    .catch(err => {
        console.log(err);
    });


app.listen(PORT, () => {
    console.log(`Started listening on port ${PORT}.`);
});