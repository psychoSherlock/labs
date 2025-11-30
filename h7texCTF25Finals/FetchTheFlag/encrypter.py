import base64
import json

_1111 = [
    "charCodeAt",   # 0 (just for mapping compatibility)
    "fromCharCode", # 1
    "length",       # 2
    "floor",        # 3
    "random",       # 4
    "stringify",    # 5
    "parse"         # 6
]

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
