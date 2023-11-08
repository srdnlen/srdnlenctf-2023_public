# Urban Odissey

## Secret retrieving
This challenge is provided with a pcapng file. After opening it, you'll find a very large file with numerous TCP and HTTP transactions.
Upon examining the TCP stream, you'll notice 26 HTTP requests with no body content. Interestingly, the HTTP responses from the server always contain different quotes about random cities worldwide. No parameters are needed to alter the server's response; it's simply a randomly selected quote from the server's pool.

```
POST / HTTP/1.1
Host: 127.0.0.1:8077
User-Agent: python-requests/2.28.1
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 0

HTTP/1.1 200 OK
Server: Werkzeug/2.3.4 Python/3.9.7
Date: Wed, 25 Oct 2023 09:52:26 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 87
Connection: close

Amsterdam's scenic canals and world-class museums make it a city best explored by bike.

```

The 26th HTTP transaction seems interesting. In this case, the request's body contains data, a string labeled "s3cr3t."


```
POST / HTTP/1.1
Host: 127.0.0.1:8077
User-Agent: python-requests/2.28.1
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 67
Content-Type: application/x-www-form-urlencoded

s3cr3t=TGF0OjE5LjA2MDc2MTk0MjAwNjk2LCBMb25nOjcyLjg1NjQ0OTc5MDA0NzA4HTTP/1.1 200 OK
Server: Werkzeug/2.3.4 Python/3.9.7
Date: Wed, 25 Oct 2023 09:52:26 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 43
Connection: close

a1pr f3perg! j0aq3e1at u0j 1 p4a q3pelcg 1g
```
For the first time, the server's response differs, offering an encrypted message. When you attempt to decrypt this message using the ROT13 algorithm, you'll uncover the text "n1ce s3cret! w0nd3r1ng h0w 1 c4n d3crypt 1t." This suggests that the secret is encrypted with some algorithm. After using base64 decoding, the content of the secret is revealed:

```
lat:19.06076194200696, Long:72.85644979004708
```

These appear to be coordinates! After searching these coordinates online, you'll discover they lead to Sant Dnyaneshwar Nagar, Bandra East, Mumbai, Maharashtra 400051, India. Interesting, but what's the significance of this information?


## Part two: Finding the correct flag

The pcapng file remains extensive, containing at least 1000 HTTP interactions. As you continue your exploration, you'll notice more empty requests. However, at a certain point, the request/response pattern changes for all subsequent interactions. Now, each request includes the name of a city within the data, and the server responds with encrypted messages that change every time.

```
POST / HTTP/1.1
Host: 127.0.0.1:8077
User-Agent: python-requests/2.28.1
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 12
Content-Type: application/x-www-form-urlencoded

city=TorontoHTTP/1.1 200 OK
Server: Werkzeug/2.3.4 Python/3.9.7
Date: Wed, 25 Oct 2023 09:52:30 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 76
Connection: close

c3JkbmxlbntiM18wbjNfZjB1cl90NGszX2IzdHczM25fbjN4dF80c2szZF93aDNyM180NTE0NX0=
```

By examining the format of the strings, it becomes apparent that these strings are encoded with base64 as well. After the decryption, you'll discover something intriguing: they resemble flag formats.

For example;
```
srdnlen{b3_0n3_f0ur_t4k3_b3tw33n_n3xt_4sk3d_wh3r3_45145}
```
But there's a catch: this quote doesn't make sense, and it's not the correct flag. 
It seems that all interactions return an incorrect flag. However, there might be a way to retrieve the correct flag using the secret you discovered earlier.

Since the coordinates led to Mumbai, and each request contains the name of a different city, you can use Wireshark's "Search String in Packet Details" tool to locate the HTTP interaction containing "Mumbai" in the HTTP request. 

It turns out that this data parameter is in stream number 494.

```
POST / HTTP/1.1
Host: 127.0.0.1:8077
User-Agent: python-requests/2.28.1
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 11
Content-Type: application/x-www-form-urlencoded

city=MumbaiHTTP/1.1 200 OK
Server: Werkzeug/2.3.4 Python/3.9.7
Date: Wed, 25 Oct 2023 09:52:32 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 80
Connection: close

c3JkbmxlbnsxdF93NHNudF90MDBfZDFmZjFjdWx0X2J1dF9NdW1iNDFfMXNfYzRoMHRpY18zMDEwMH0=
```
After decoding the server's response with base64, the correct flag was revealed:
```
srdnlen{1t_w4snt_t00_d1ff1cult_but_Mumb41_1s_c4h0tic_30100}
```
