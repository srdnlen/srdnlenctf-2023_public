const mongoose = require('mongoose')
const passportLocalMongoose = require('passport-local-mongoose')

const userSchema = new mongoose.Schema({
    username: {
        type: String,
        required: true
    },
    passwd: {
        type: String
    },
    fighters: {
        type: [{
            type: mongoose.Schema.Types.ObjectId,
            ref: 'PugFighter'
        }]
    }
})

userSchema.plugin(passportLocalMongoose, {
    session: false
})

module.exports = mongoose.model('User', userSchema)
