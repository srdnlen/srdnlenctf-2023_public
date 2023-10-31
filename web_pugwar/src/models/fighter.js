const mongoose = require('mongoose')

const fighterSchema = new mongoose.Schema({
    player: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    fighterId: {
        type: Number,
        required: true,
        index: true,
        unique: true
    },
    pugName: {
        type: String,
        required: true,
        default: ''
    },
    ability: {
        type: String,
        required: true,
        default: ''
    },
    secret: {
        type: String,
        required: false,
        default: ''
    }
})

module.exports = mongoose.model('PugFighter', fighterSchema)
