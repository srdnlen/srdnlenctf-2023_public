require("express-async-errors");

const express = require("express");
const bot = require("./bot");

const PORT = 9999;
const BLOG_URL = process.env["BLOG_URL"] || "http://localhost:3000";
const app = express();

app.use(express.json());

app.post("/visit", async function (req, res) {
  const url = req.body.url;

  if (!url || typeof url !== "string") {
    console.log("Visit requested with missing parameters");
    res.status(400).send("Missing parameters");
    return;
  }

  if (url.startsWith(BLOG_URL)) {
    try {
      await bot.visit(url);
      res.send("ok");
    } catch (e) {
      console.log(e);
      res.status(500).send("failed");
      return;
    }
  } else {
    res.status(400).send("Bad url");
  }
});

app.listen(PORT, "0.0.0.0");
console.log("Listening on port %d ...", PORT);
