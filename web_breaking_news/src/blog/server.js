const express = require("express");
const path = require("path");
const jwt = require("jsonwebtoken");
const { privKey } = require("./utils/authorization.js");
const middleware = require("./utils/JWTHelper.js");
const db = require("./utils/database.js");
const bcrypt = require("bcryptjs");
const cookieParser = require("cookie-parser");

const BOT_URL = process.env["BOT_URL"] || "http://localhost:9999/visit";
const PORT = 3000;

const app = express();

// Setting paths
app.use("/static", express.static(path.join(__dirname, "static")));

// Configurations
app.use(express.urlencoded({ extended: false }));
app.set("view engine", "ejs");

app.set("views", path.join(__dirname, "views"));

app.use((_req, res, next) => {
  res.locals.errormsg = undefined;
  res.locals.successmsg = undefined;
  next();
});

app.use(cookieParser());

// App routes
app.get("/news", middleware, async (req, res) => {
  try {
    const decoded = jwt.decode(req.cookies.session);
    const userId = decoded.id;
    const username = decoded.username;

    if (userId == 1 && username == "admin") {
      news = await db.News.findAll();
      return res.render("news", { news });
    } else {
      news = await db.News.findAll({
        where: { reserved: false },
      });
      return res.render("news", { news });
    }
  } catch (error) {
    console.error(error);
    res.status(500).send("Something went wrong!");
  }
});

app.get("/logout", async (_req, res) => {
  res.clearCookie("session");
  const message = {
    msg: null,
  };
  res.render("login", { message });
});

app.get("/", async (_req, res) => {
  let message = {
    msg: null,
  };
  res.render("login", { message });
});

app.post("/", async (req, res) => {
  try {
    const username = req.body.username;
    const password = req.body.password;

    if (!username || !password) {
      const message = {
        msg: "Username and password are required",
      };
      return res.render("login", { message });
    }

    let user = await db.Users.findOne({
      where: { username: username },
    });

    if (!user) {
      let message = {
        msg: "Invalid username or password",
      };
      return res.render("login", { message });
    }

    let validPassword = bcrypt.compareSync(password, user.password);
    if (!validPassword) {
      let message = {
        msg: "Invalid username or password",
      };
      return res.render("login", { message });
    }
    const token = jwt.sign({ id: user.id, username: user.username }, privKey, {
      expiresIn: "1h",
      algorithm: "RS256",
    });

    res.cookie("session", token);
    res.redirect("/news");
  } catch (error) {
    console.error(error);
    res.status(500).send({
      error: "Something went wrong!",
    });
  }
});

app.get("/register", async (_req, res) => {
  const message = {
    msg: null,
  };
  res.render("register", { message });
});

app.post("/register", async (req, res) => {
  try {
    const username = req.body.username;
    const password = req.body.password;

    if (!username || !password) {
      const message = {
        msg: "Username and password are required",
      };
      return res.render("register", { message });
    }
    const existingUser = await db.Users.findOne({
      where: { username: username },
    });
    if (existingUser) {
      const message = {
        msg: "Username already exists",
      };
      return res.render("register", { message });
    }

    await db.Users.create({
      username: username,
      password: bcrypt.hashSync(password),
    }).then(() => {
      res.redirect("/");
    });
  } catch (error) {
    console.error(error);
    res.status(500).send({
      error: "Something went wrong!",
    });
  }
});

app.get("/report", middleware, async (_req, res) => {
  let message = {
    msg: null,
  };
  res.render("report", { message });
});

app.post("/report", middleware, async (req, res) => {
  try {
    const url_to_visit = req.body.url;
    if (!url_to_visit) {
      message = {
        error: "URL is needed!!",
      };
      res.render("report", { message });
    } else {
      let result = await fetch(BOT_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: url_to_visit }),
      });

      if (result.status == 200) {
        message = {
          msg: "An Admin will visited your url",
        };
        return res.render("report", { message });
      } else if (result.status == 400) {
        message = {
          error: "Bad Url",
        };
        return res.render("report", { message });
      } else {
        message = {
          error: "Admin failed to visit the URL",
        };
        return res.render("report", { message });
      }
    }
  } catch (error) {
    console.error(error);
    res.status(500).send({
      error: "Something went wrong!",
    });
  }
});

// Startup
(async () => {
  try {
    await db.connect();
    await db.create();
    app.listen(PORT, () => {
      console.log("Listening on port %d ...", PORT);
    });
  } catch (error) {
    console.error(error);
  }
})();
