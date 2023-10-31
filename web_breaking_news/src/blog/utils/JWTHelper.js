const { Session } = require("inspector");
const jwt = require("jsonwebtoken");
const db = require("./database");
const { pubKey } = require("./authorization");

const middleware = async (req, res, next) => {
  try {
    Sessioncookie = req.cookies.session;

    if (!Sessioncookie) {
      return res.redirect("/");
    }
    const decoded = jwt.decode(Sessioncookie, { complete: true });
    if (decoded.header.alg == "RS256") {
      try {
        const user = jwt.verify(Sessioncookie, pubKey, {
          algorithms: [decoded.header.alg],
        });
        if (
          !(await db.Users.findOne({
            where: { id: user.id, username: user.username },
          }))
        ) {
          return res.status(403).send("No active username! Register one!");
        }
      } catch (err) {
        res.redirect("/");
      }
    } else {
      res.redirect("/");
    }
  } catch (err) {
    console.error(err);
    return res.redirect("/");
  }
  next();
};

module.exports = middleware;
