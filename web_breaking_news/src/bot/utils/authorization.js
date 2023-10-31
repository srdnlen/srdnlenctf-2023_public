const fs = require("fs");
const path = require("path");

const pubKey = fs.readFileSync(path.join(__dirname, "pubKey.pem"), "utf-8");
const privKey = fs.readFileSync(path.join(__dirname, "privKey.pem"), "utf-8");

module.exports = { pubKey, privKey };
