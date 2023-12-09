import hashlib
import hmac

def hamc_encrypt(message, key):

    # result1 = hmac.new(key.encode(), message.encode(), hashlib.md5).hexdigest()
    result2 = hmac.new(key.encode(), message.encode(), hashlib.sha1).hexdigest()
    # result3 = hmac.new(key.encode(), message.encode(), hashlib.sha1).digest()
    # _sig = base64.b64encode(result3).decode()
    
    # print(result1)
    # print(result2)
    # print(_sig)

    return result2

if __name__ == "__main__":
    str = "114514"
    key = "3bbca8e69ad52e11c12242d144bd6bd6"
    print(hamc_encrypt(str, key))
