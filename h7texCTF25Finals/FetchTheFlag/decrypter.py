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
