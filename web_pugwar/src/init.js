const { DB, App } = require('./server/app')
const port = process.env.PORT || 3000
const databasename = 'pugwar'
const uri = process.env.MONGO_CONNECTION_URI || `mongodb://127.0.0.1:27017/${databasename}`

DB(uri, databasename).then(async () => {
    console.log('Im in')
    const app = await App()
    console.log(`Initializing... `)
    app.listen(port, () => {
        console.log(`Listening on port ${port}`)
    })
})
