//Require Mongoose
var mongoose = require('mongoose');

//Define a schema
var Schema = mongoose.Schema;

var ProcessedSchema = new Schema({
    data: Object
});

//compile schema into a model
var Processed = mongoose.model("Processed", ProcessedSchema);

module.exports = Processed;
