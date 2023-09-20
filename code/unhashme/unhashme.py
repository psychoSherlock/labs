# Date: 20/09/2023
# Author: psychoSherlock
# Website: psychoSherlock.github.io
# Linkedin: https://www.linkedin.com/in/athul-prakash-nj-564a80226/

import hashlib


def hashme(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()

def verify_key(key):
    if len(key) != 7 and (key[2] and key[4] != '.'):
        return False
    
    part1 = key[:4]
    part2 = key[4:]
    
    hash1 = hashme(part1)
    hash2 = hashme(part2)
    
    target_hash1 = "f4bfe0e6c39943f1a630458f43668c31"
    target_hash2 = "a4e49d067580bcbfa42d6895861d93d6"
    
    if hash1 == target_hash1 and hash2 == target_hash2:
        return True
    else:
        return False

if __name__ == "__main__":

    password = input('Password: ')
    
    if verify_key(password):
        print("Congratulations! You just unhashed me! Follow me for more such challanges: https://github.com/psychoSherlock")
    else:
        print("Whoopsie!! Wrong answer!!")
