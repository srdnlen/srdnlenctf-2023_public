const path = require('path')
const bodyParser = require('body-parser')
const mongoose = require('mongoose')
const express = require('express')
const User = require('../models/user')
const Pug = require('../models/pug')
const passport = require('passport')
const { engine } = require('express-handlebars')
const Fighter = require('../models/fighter')
const { Strategy: JwtStrategy } = require('passport-jwt')
const cookieParser = require('cookie-parser')

function DB(DB_URI, dbName) {
    return new Promise((res, _) => {
        mongoose.set('strictQuery', false);
        mongoose.connect(DB_URI, {useNewUrlParser: true, useUnifiedTopology: true, dbName}).then(() => res())
    })
}

async function App() {
    const app = express()
    app.use(passport.initialize())
    app.use(cookieParser())


    app.use(bodyParser.json())

    app.engine('hbs', engine({extname: '.hbs', defaultLayout: 'base'}))

    app.use(express.static('static'));
    app.set('view engine', 'hbs')
    app.set('views', path.join(__dirname, '../webviews'))

    app.use('/', require('./routes'))
    
    passport.use('user-local', User.createStrategy())
    const option = {secretOrKey: process.env.JWT_SECRET, jwtFromRequest: (req) => req?.cookies?.['jwt'], algorithms: ['HS256']}

    passport.use(
        new JwtStrategy(option, (payload, next) => {
            User.findOne({ _id: payload.userId })
                .then((user) => {
                    next(null, { userId: user._id } || false)
                }).catch((_) => next(null, false))
        })
    )

    let administrator = await User.findOne({ username: '0CTAVIUS' })
    if(!administrator) {
        administrator = new User({ username: '0CTAVIUS' })
        await administrator.save()
    }

    let fighter = await Fighter.findOne({ fighterId: 1 })
    Pepito = new Pug({pugName: "Pepito", abilities: "He snores very loudly"})
    Broccolo = new Pug({pugName: "Broccolo", abilities: "Can sleep 16 hours straight"})
    Michele = new Pug({pugName: "Michele", abilities: "Database expert"})
    Mario = new Pug({pugName: "Mario", abilities: "He knows how to keep secrets"})

    await Pepito.save()
    await Broccolo.save()
    await Michele.save()
    await Mario.save()



    if(!fighter) {
        const FLAG = process.env.FLAG || 'SRDNLEN{this_is_the_real_flag}'
        fighter = new Fighter({ fighterId: 1, player: administrator._id, pugName: "Mario", ability: "He knows how to keep secrets", secret: FLAG })
        await fighter.save()
        
        administrator.fighters.push(fighter)
        await administrator.save()
    }

    app.use('/', (req, res) => {
        res.status(404)
        if(req.accepts('html') || req.accepts('json')) {
            return res.render('notfound')
        }
    })

    return app
}



module.exports = {DB,App}
