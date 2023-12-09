import hashlib

def md5_encrypt(text, salt):
    # 加盐，时间戳
    md5 = hashlib.md5()
    md5.update((text + salt).encode('utf-8'))
    md5str = md5.hexdigest()
    return md5str

if __name__ == "__main__":
    text = 'zwb'
    print(md5_encrypt(text))
