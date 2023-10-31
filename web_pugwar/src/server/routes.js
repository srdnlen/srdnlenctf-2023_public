const express = require('express')
const User = require('../models/user')
const Pug = require('../models/pug')
const isAuth = (req, res, next) => {passport.authenticate('jwt', { session: false, failureRedirect: '/user-login' })(req, res, next)}
const Fighter = require('../models/fighter')
const JWT = require('jsonwebtoken')
const router = express.Router()
const passport = require('passport')
const pug = require('../models/pug')

router.get('/halloffame', isAuth, async (req, res) => {
    try{
        const all = await Pug.find()
        const pugs = []
        for(let p of all) {
            pugs.push({ pugName: p.pugName, abilities: p.abilities })
        }
        return res.render('halloffame', { Autenticated: true, pugs: pugs})
    } catch{
        return res.render('error', { Autenticated: true, message: 'Error during request' })
    }
})

router.get('/register-user', (req, res) => {
    return res.render('register-user')
})

router.post('/register-user', (req, res, next) => {
    let { username , password } = req.body
    if (username == null || password == null){
        return next({message: "Error"})
    }
    if(!username || !password) {
        return next({ message: 'You forgot to enter your credentials!' })
    }
    if(password.length <= 2) {
        return next({ message: 'Please choose a longer password.. :-(' })
    }

    User.register(new User({ username }), password, (err, user) => {
        if(err && err.toString().includes('registered')) {
            return next({ message: 'Username taken' })
        } else if(err) {
            return next({ message: 'Error during registration' })
        }

        const jwtoken = JWT.sign({userId: user._id}, process.env.JWT_SECRET, {algorithm: 'HS256',expiresIn: '10h'})
        res.cookie('jwt', jwtoken, { httpOnly: true })

        return res.json({success: true, message: 'Account registered.'})
    })
})

router.get('/user-login', (req, res) => {
    return res.render('user-login')
})

router.post('/user-login', (req, res, next) => {
    passport.authenticate('user-local', (_, user, err) => {
        if(err) {
            return next({ message: 'Error during login' })
        }

        const jwtoken = JWT.sign({userId: user._id}, process.env.JWT_SECRET, {algorithm: 'HS256',expiresIn: '10h'})
        res.cookie('jwt', jwtoken, { httpOnly: true })

        return res.json({
            success: true,
            message: 'Logged'
        })
    })(req, res, next)
})

router.get('/user-logout', (req, res) => {
    res.clearCookie('jwt')
    res.redirect('/')
})




router.get('/choose-fighters', isAuth, async (req, res) => {
        return res.render('choose-fighters', { Autenticated: true })
})

router.post('/choose-fighters', isAuth, async (req, res, next) => {
    let { pugName, ability, secret } = req.body

    if(pugName == null || ability == null || secret == null){
        return next({ message: 'Error'})
    }

    if(!ability || ability.length > 100) {
        return next({ message: 'Ability Error' })
    }

    if(!pugName || pugName === 'Mario' || pugName === 'Broccolo' || pugName === 'Pepito' || pugName === 'Michele'){
        return next({ message: 'NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO' })
    }

    pugName = pugName.toString()
    secret = secret.toString()
    ability = ability.toString()
    try {
        const user = await User.findById(req.user.userId)
        const fighterId = Math.floor(Math.random() * 10000)

        const fighter = new Fighter({ player: user._id, fighterId: fighterId, pugName: pugName, ability: ability, secret: secret})

        await fighter.save()

        user.fighters.push(fighter._id)
        await user.save()

        return res.json({
            success: true,
            message: 'This is a good fighter..'
        })
    } catch {
        return next({ message: 'Error during fighter choose' })
    }
})

router.get('/fighter-customization', isAuth, async (req, res) => {
    let nosql = req.query

    try {
        if('fighterId' in nosql && nosql.fighterId === 1){
            return res.render('error', { Autenticated: true, message: 'No Way lol' })
        }
        if('pugName' in nosql) {
            const Fight = await Fighter.findOne(nosql)

            if(!Fight) {
                return res.render('error', { Autenticated: true, message: 'There are no fighters with that pugName!' })
            }

            if(Fight.player.toString() != req.user.userId.toString()) {
                return res.render('error', { Autenticated: true, message: 'You can\'t customize other players fighter!' })
            }

            res.render('fighter-customization', { Autenticated: true, pugName: Fight.pugName, ability: Fight.ability })
        } else {
            return res.render('error', { Autenticated: true, message: 'Error during request' })
        }
    } catch {
        return res.render('error', { Autenticated: true, message: 'Error during request' })
    }
})

router.post('/fighter-customization', isAuth, async (req, res, next) => {
    let nosql = req.query

    try {
        if(null in req.query){
            return next('Error')
        }
        if('pugName' in nosql) {
            const fighter = await Fighter.findOne(nosql)

            if(!fighter) {
                return next({ message: 'There are no fighters with that pugName!' })
            }

            if(fighter.player.toString() != req.user.userId.toString()) {
                return next({ message: 'You can\'t customize other players fighter!' })
            }

            let { ability } = req.body
            if(!ability || ability.length > 100) {
                return next({ message: 'Ability Error' })
            }



            ability = ability.toString()
            fighter.ability = ability
            await fighter.save()


            return res.json({ success: true, message: 'Fighter has been correctly customized!' })
        } else {
            return next({ message: 'Error during request' })
        }
    } catch(e) {
        return next({ message: 'Error during request' })
    }
})

router.get('/', (req, res, next) => {
    passport.authenticate('jwt', async (err, r) => {
        let { userId } = r
        if(!userId) {
            return res.render('home', {
                Autenticated: false
            })
        }

        const user = await User.findById(userId).populate('fighters').exec()
        const fighters = []


        for(let f of user.fighters) {
            fighters.push({ fighterId: f.fighterId, pugName: f.pugName, ability: f.ability, secret: f.secret })
        }
        return res.render('home', {
            Autenticated: true,
            username: user.username,
            fighters: fighters
        })
    })(req, res, next)
})

router.use((err, req, res, next) => {
    res.status(err.status || 400).json({
        success: false,
        error: err.message || 'Invalid Request - The Pug is getting angry..',
    })
})

module.exports = router

