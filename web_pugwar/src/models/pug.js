const mongoose = require('mongoose')

const pugSchema = new mongoose.Schema({
    pugName: {
        type: String,
        required: true,
        unique: true
    },
    abilities: {
        type: String,
        required: true,
        default: ''
    }
})

module.exports = mongoose.model('Pug', pugSchema)
