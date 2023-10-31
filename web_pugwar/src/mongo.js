var UsernameRoot = process.env.MONGO_INITDB_ROOT_USERNAME;
var PasswordRoot = process.env.MONGO_INITDB_ROOT_PASSWORD;
var ADMINISTRATOR = db.getSiblingDB('admin');
ADMINISTRATOR.auth(UsernameRoot, PasswordRoot);
var DBPass = process.env.MONGO_INITDB_PASSWORD;
var DBUser = process.env.MONGO_INITDB_USERNAME;
db.createUser({ user: DBUser, pwd: DBPass, roles: ["readWrite"]});