# Fetch The Flag

**Points:** 1000

**Author:** psychoSherlock

---

## Description

Go on! Fetch The Flag 🙂

---

## Writeup & Solution

So this one is meant to be really easy and warm for the players. I know some might have found it related to cryptography but it's not really! The crypto part is not the goal, the actual goal is to find the vulnerability. Crypto part you can solve easily with any available AI.

### 1. Initial Analysis

Now the challenge gives you a web interface with just one button: **Fetch The Flag**.

If you click the button, the following flag will be displayed:

```
H7CTF{F4K3_FL4G_N1C3_TRY_D1DDY}
```

If you checked the Burp history for anything interesting, you'll see the following request had been sent with the following response:

**Request:**

```http
POST /api/flag HTTP/1.1
Host: localhost:3000
Content-Length: 35
sec-ch-ua-platform: "Linux"
Accept-Language: en-GB,en;q=0.9
sec-ch-ua: "Not A(Brand";v="8", "Chromium";v="132"
Content-Type: application/json
sec-ch-ua-mobile: ?0
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36
Accept: */*
Origin: http://localhost:3000
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:3000/
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

{"data":"NytkHGByZiQ/eR9te1YAFBo="}
```

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
ETag: "14ksfyr8byv1v"
Content-Length: 67
Vary: Accept-Encoding
Date: Sun, 30 Nov 2025 05:57:46 GMT
Connection: keep-alive
Keep-Alive: timeout=5

{"data":"S2NpLhlWaLR5fA9adFceAAFKTWla5EVcC3wKbghA5WkBfgdDb3VRABQa"}
```

Not much hard to deduce that there is some kind of encryption happening here. But if you tried to look at the source code, you'll find it's obfuscated.

---

### 2. Deobfuscation Methods

There are multiple ways to deobfuscate the JavaScript files. What most players did, as I observed, was that they used [obf-io.deobfuscate.io](https://obf-io.deobfuscate.io/) to deobfuscate.

Yes, you can do that as there is no general rule on HOW TO PLAY the CTF. But what I meant to solve it was using the **JavaScript Source Mapping** method. I only saw very few people solving using that way, so here is the intended method:

#### What are Source Maps?

Source maps (`.map` files) are debugging aids that map minified/obfuscated production code back to the original source code. When developers build their applications, tools like Webpack or Next.js generate these map files alongside the bundled JavaScript.

**How they work:**

- The minified JS file contains a comment: `//# sourceMappingURL=file.js.map`
- This `.map` file contains the complete original source code structure
- Browsers use this to show readable code in DevTools

**Security Risk:**  
If source maps are left exposed in production (which happens more often than you'd think), attackers can:

- Retrieve the complete original source code
- Understand the application logic
- Find hardcoded secrets, keys, or vulnerabilities

---

### 3. Extracting Source Maps

You can use any source mapping tool, but what I usually go with is [sourcemapper](https://github.com/denandz/sourcemapper).

Now you just need to use the tool. You might face this error:

```bash
└─$ sourcemapper -url http://localhost:3000/_next/static/chunks/pages/index-fd006164ce8ea2bd.js.map -output index
2025/11/30 11:40:49 [+] Retrieving Sourcemap from http://localhost:3000/_next/static/chunks/pages/index-fd006164ce8ea2bd.js.map...
2025/11/30 11:40:49 [+] Read 39539 bytes, parsing JSON.
2025/11/30 11:40:49 [+] Retrieved Sourcemap with version 3, containing 8 entries.
2025/11/30 11:40:49 [+] Writing 271 bytes to index/_N_E.
2025/11/30 11:40:49 [+] Writing 472 bytes to index/_N_E/utils/buttonObserver.js.
2025/11/30 11:40:49 Error writing index/_N_E/utils/buttonObserver.js file: open index/_N_E/utils/buttonObserver.js: not a directory
2025/11/30 11:40:49 [+] Writing 2220 bytes to index/_N_E/utils/cryptoUtils.ts.
2025/11/30 11:40:49 Error writing index/_N_E/utils/cryptoUtils.ts file: open index/_N_E/utils/cryptoUtils.ts: not a directory
2025/11/30 11:40:49 [+] Writing 1668 bytes to index/_N_E/utils/flagInterceptor.ts.
2025/11/30 11:40:49 Error writing index/_N_E/utils/flagInterceptor.ts file: open index/_N_E/utils/flagInterceptor.ts: not a directory
2025/11/30 11:40:49 [+] Writing 7266 bytes to index/_N_E/components/DecryptedText.tsx.
2025/11/30 11:40:49 Error writing index/_N_E/components/DecryptedText.tsx file: open index/_N_E/components/DecryptedText.tsx: not a directory
2025/11/30 11:40:49 [+] Writing 6700 bytes to index/_N_E/components/LetterGlitch.jsx.
2025/11/30 11:40:49 Error writing index/_N_E/components/LetterGlitch.jsx file: open index/_N_E/components/LetterGlitch.jsx: not a directory
2025/11/30 11:40:49 [+] Writing 3028 bytes to index/_N_E/pages/index.tsx.
2025/11/30 11:40:49 Error writing index/_N_E/pages/index.tsx file: open index/_N_E/pages/index.tsx: not a directory
panic: runtime error: index out of range [7] with length 7

```

**Why does this error occur?**

The sourcemapper tool first writes a file named `_N_E` (containing 271 bytes of data). Then it tries to write files inside `_N_E/utils/` as if `_N_E` were a directory. Since `_N_E` already exists as a file, the tool can't create subdirectories inside it. This is a quirk in how Next.js structures its source maps, where `_N_E` serves as both a namespace entry and a path prefix.

You can fix this by creating a `_N_E` directory manually:

```bash
──(psychosherlock㉿fsociety)-[/tmp]
└─$ rm index/_N_E

┌──(psychosherlock㉿fsociety)-[/tmp]
└─$ mkdir index/_N_E

┌──(psychosherlock㉿fsociety)-[/tmp]
└─$ sourcemapper -url http://localhost:3000/_next/static/chunks/pages/index-fd006164ce8ea2bd.js.map -output index
2025/11/30 11:42:00 [+] Retrieving Sourcemap from http://localhost:3000/_next/static/chunks/pages/index-fd006164ce8ea2bd.js.map...
2025/11/30 11:42:00 [+] Read 39539 bytes, parsing JSON.
2025/11/30 11:42:00 [+] Retrieved Sourcemap with version 3, containing 8 entries.
2025/11/30 11:42:00 [+] Writing 271 bytes to index/_N_E.
2025/11/30 11:42:00 Error writing index/_N_E file: open index/_N_E: is a directory
2025/11/30 11:42:00 [+] Writing 472 bytes to index/_N_E/utils/buttonObserver.js.
2025/11/30 11:42:00 [+] Writing 2220 bytes to index/_N_E/utils/cryptoUtils.ts.
2025/11/30 11:42:00 [+] Writing 1668 bytes to index/_N_E/utils/flagInterceptor.ts.
2025/11/30 11:42:00 [+] Writing 7266 bytes to index/_N_E/components/DecryptedText.tsx.
2025/11/30 11:42:00 [+] Writing 6700 bytes to index/_N_E/components/LetterGlitch.jsx.
2025/11/30 11:42:00 [+] Writing 3028 bytes to index/_N_E/pages/index.tsx
```

Notice the new files. There are two interesting ones:

```bash
┌──(psychosherlock㉿fsociety)-[/tmp]
└─$ ls index/_N_E/utils
buttonObserver.js  cryptoUtils.ts  flagInterceptor.ts
```

---

### 4. Analyzing the Crypto Logic

Now read the `cryptoUtils.ts` file and you'll find another slightly less obfuscated file:

```js
const _0x1111 = [
  "charCodeAt",
  "fromCharCode",
  "length",
  "floor",
  "random",
  "stringify",
  "parse",
] as const;
const _0x2222 =
  "d124f56bcbf01e6c9ed55be74df1fe5cac01adf9daacd5629cfa7ee3e1490247499e7a2af6b11ac5524f6b11759ebd90a7782c77ab183ee14b710dd8f5ac78fa";
const _0x3333 =
  "64a4a0bb067e2848f082da7026da5341905ed4b80b2599c025a04fcb2b9adb59";

function _0xa7c2(a: string, b: string): string {
  let r = "";
  for (let i = 0; i < (a as any)[_0x1111[2]]; i++) {
    r += (String as any)[_0x1111[1]](
      (a as any)[_0x1111[0]](i) ^
        (b as any)[_0x1111[0]](i % (b as any)[_0x1111[2]])
    );
  }
  return r;
}

function _0x9e5f(s: string, n: number): string {
  let r = "";
  for (let i = 0; i < (s as any)[_0x1111[2]]; i++) {
    const c = (s as any)[_0x1111[0]](i);
    r += (String as any)[_0x1111[1]]((c + n) % 256);
  }
  return r;
}

function _0x6b1d(s: string): string {
  return s.split("").reverse().join("");
}

function _0x2f8c(d: string, k: string, iv: string): string {
  const s1 = _0xa7c2(d, k);
  const s2 = _0x9e5f(s1, 13);
  const s3 = _0xa7c2(s2, iv);
  const s4 = _0x6b1d(s3);
  return s4;
}

function _0x4e7a(d: string, k: string, iv: string): string {
  const s1 = _0x6b1d(d);
  const s2 = _0xa7c2(s1, iv);
  const s3 = _0x9e5f(s2, -13);
  const s4 = _0xa7c2(s3, k);
  return s4;
}

function _0x1c3b(s: string): string {
  if (typeof Buffer !== "undefined") {
    return Buffer.from(s, "binary").toString("base64");
  } else {
    return btoa(s);
  }
}

function _0x5d9e(s: string): string {
  if (typeof Buffer !== "undefined") {
    return Buffer.from(s, "base64").toString("binary");
  } else {
    return atob(s);
  }
}

export function _0x4444(data: any): string {
  const jsonStr = (JSON as any)[_0x1111[5]](data);
  const _0x6666 = _0x2f8c(jsonStr, _0x2222, _0x3333);
  return _0x1c3b(_0x6666);
}

export function _0x5555(encryptedData: string): any {
  try {
    const decoded = _0x5d9e(encryptedData);
    const _0x7777 = _0x4e7a(decoded, _0x2222, _0x3333);
    return (JSON as any)[_0x1111[6]](_0x7777);
  } catch (e) {
    throw new Error("failed");
  }
}

const _fn = {
  e: _0x4444,
  d: _0x5555,
};

export const encrypt = _fn.e;
export const decrypt = _fn.d;

```

---

### 5. Creating the Python Scripts

Now this is the part where some people started doing cryptography and all, but no need to do that. Just use an AI and you'll get an `encrypter.py` as well as a `decrypter.py` — these small conversions are simple to do.

**decrypter.py:**

```python
import base64
import json

_2222 = "d124f56bcbf01e6c9ed55be74df1fe5cac01adf9daacd5629cfa7ee3e1490247499e7a2af6b11ac5524f6b11759ebd90a7782c77ab183ee14b710dd8f5ac78fa"
_3333 = "64a4a0bb067e2848f082da7026da5341905ed4b80b2599c025a04fcb2b9adb59"


def a7c2(a: str, b: str) -> str:  # XOR
    return ''.join(chr(ord(a[i]) ^ ord(b[i % len(b)])) for i in range(len(a)))


def n9e5f(s: str, n: int) -> str:  # shift by n
    return ''.join(chr((ord(c) + n) % 256) for c in s)


def reverse_str(s: str) -> str:
    return s[::-1]


def e4e7a(d: str, k: str, iv: str) -> str:
    s1 = reverse_str(d)
    s2 = a7c2(s1, iv)
    s3 = n9e5f(s2, -13)
    s4 = a7c2(s3, k)
    return s4


def decrypt(token: str):
    try:
        decoded = base64.b64decode(token).decode("latin1")
        raw = e4e7a(decoded, _2222, _3333)
        return json.loads(raw)
    except:
        raise ValueError("failed")


if __name__ == "__main__":
    test = input("Paste encrypted string: ")
    print("Decrypted:", decrypt(test))
```

**encrypter.py:**

```python
import base64
import json

_2222 = "d124f56bcbf01e6c9ed55be74df1fe5cac01adf9daacd5629cfa7ee3e1490247499e7a2af6b11ac5524f6b11759ebd90a7782c77ab183ee14b710dd8f5ac78fa"
_3333 = "64a4a0bb067e2848f082da7026da5341905ed4b80b2599c025a04fcb2b9adb59"


def a7c2(a: str, b: str) -> str:  # XOR
    res = []
    for i in range(len(a)):
        res.append(chr(ord(a[i]) ^ ord(b[i % len(b)])))
    return ''.join(res)


def n9e5f(s: str, n: int) -> str:  # shift by n mod256
    return ''.join(chr((ord(c) + n) % 256) for c in s)


def reverse_str(s: str) -> str:
    return s[::-1]


def f2f8c(d: str, k: str, iv: str) -> str:
    s1 = a7c2(d, k)
    s2 = n9e5f(s1, 13)
    s3 = a7c2(s2, iv)
    s4 = reverse_str(s3)
    return s4


def encrypt(data):
    json_str = json.dumps(data)
    encrypted = f2f8c(json_str, _2222, _3333)
    return base64.b64encode(encrypted.encode("latin1")).decode("utf8")


if __name__ == "__main__":
    print("Encrypted:", encrypt(input("Enter string to encrypt: ")))
```

---

### 6. Exploiting the Vulnerability

Run the decrypter on the data sent by the client to `/api/flag`:

```bash
└─$ python3 decrypter.py
Paste encrypted string: NytkHGByZiQ/eR9te1YAFBo=
Decrypted: {'fakeFlag': True}
```

Now just change that to:

```python
{"fakeFlag": false}
```

And encrypt it:

```bash
└─$ python3 encrypter.py
Enter string to encrypt: {"fakeFlag": false}
Encrypted: QGc2EwQ3SWoqQTkmLFMCW3VrQ2Nl
```

Replace the data part with this one and send the request:

```json
{ "data": "QGc2EwQ3SWoqQTkmLFMCW3VrQ2Nl" }
```

You'll get a response with the real flag. Decrypt the response:

```bash
└─$ python3 decrypter.py
Paste encrypted string: NxdnWT8oPWhycS8gJGoGTF41UX8da1ond2s7IgRvaQNUfSIlKCcDGDgoN3UBeARmICcmWD8BTl0tECkTLiRQdmtVeWYpenRXBgcVUUUqPj1FIS18Nm4IQOVpAX4HQ291UQAUGg==
Decrypted: {'flag': 'H7CTF{b4uh_y0u_br0k3_th3_c0d3_0r_th3_c0de_br0ke_y0u_f132066b-28c6-4941-9f49-8a6291c2e612}'}
```

---

## Flag

```
H7CTF{b4uh_y0u_br0k3_th3_c0d3_0r_th3_c0de_br0ke_y0u_f132066b-28c6-4941-9f49-8a6291c2e612}
```
