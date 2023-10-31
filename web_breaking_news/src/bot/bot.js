const puppeteer = require("puppeteer");
const { privKey } = require("./utils/authorization.js");
const jwt = require("jsonwebtoken");

const TIMEOUT = 1000 * 10;

async function visit(url) {
  console.log('Running browser to visit "%s"', url);

  const browser = await puppeteer.launch({
    headless: "old",
    args: [
      "--disable-default-apps",
      "--disable-extensions",
      "--disable-gpu",
      "--disable-sync",
      "--disable-translate",
      "--hide-scrollbars",
      "--metrics-recording-only",
      "--mute-audio",
      "--no-first-run",
      "--no-sandbox",
      "--safebrowsing-disable-auto-update",
    ],
    executablePath: "/usr/bin/google-chrome",
  });

  let page = await browser.newPage();
  page.setDefaultNavigationTimeout(TIMEOUT);

  try {
    // Authentication
    const admin_cookie = jwt.sign({ id: 1, username: "admin" }, privKey, {
      expiresIn: "1h",
      algorithm: "RS256",
    });

    await page.setCookie({
      name: "session",
      httpOnly: false,
      value: admin_cookie,
      domain: "breaking-news",
    });

    // Visiting
    console.log(`Bot is visiting ${url}`);

    await page.goto(url);
    await new Promise((resolve) => setTimeout(resolve, TIMEOUT));
    await page.close();
    await browser.close();

    return "ok";
  } catch (e) {
    await browser.close();
    console.log(e);
    throw e;
  }
}

module.exports = { visit };
