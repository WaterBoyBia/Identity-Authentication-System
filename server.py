import socket
import ssl
import os
import time
from HMAC import hamc_encrypt
from md5 import md5_encrypt

def get_user_pwd():
    # 接收客户端消息
    client_message = ssl_client_socket.recv(1024)  
    global user 
    user = client_message.decode('utf-8')    
    print(user)

    # 请求密码
    ssl_client_socket.send("请输入密码：".encode('utf-8'))

    # 接收客户端消息
    client_message = ssl_client_socket.recv(1024)
    global pwd
    pwd = client_message.decode('utf-8')       
    print(pwd)

    global data

    if os.path.isfile('./account/' + user + '.txt'):
        with open('./account/' + user + '.txt', 'r', encoding='utf-8') as f:
            data = f.read()
    else:
        data = None

    if os.path.isfile('./account/salt/' + user + '.txt'):
        with open('./account/salt/' + user + '.txt', 'r', encoding='utf-8') as f:
            salt = f.read()

    # 密码验证：将账号md5加密获得散列值作为HMAC的密钥，使用HMAC对密码进行加密，
    # digestmod 模式选择为 hashlib.sha1，返回的数据是长度40位

    user_md5 = md5_encrypt(user, salt)
    global pwd_hamc
    pwd_hamc = hamc_encrypt(pwd, user_md5)


            
# 创建 socket 对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名和端口
host = 'localhost'
port = 12345

flag = 1

# 绑定地址和端口
server_socket.bind((host, port))

# 设置最大连接数
server_socket.listen(5)

print('等待客户端连接...')

while True:
    # 建立客户端连接
    client_socket, addr = server_socket.accept()
    print('连接地址：', addr)

    # 创建SSL包装的socket
    ssl_client_socket = ssl.wrap_socket(client_socket, keyfile='server-key.key', certfile='server-cert.pem', server_side=True)

    while True:
        # 选择注册或者登录
        ssl_client_socket.send("登录请输入1，注册请输入0：".encode('utf-8'))
        client_message = ssl_client_socket.recv(1024)  
        choice = client_message.decode('utf-8')
    
        if choice == '1':  # 登录
            while True:
                if flag:
                    # 请求用户名
                    ssl_client_socket.send("请输入用户名：".encode('utf-8'))
                else:
                    break
                
                get_user_pwd()  # 第一次获取用户名和密码

                if data == pwd_hamc and os.path.isfile('./account/' + user + '.txt'):
                    ssl_client_socket.send((user + "登陆成功！").encode('utf-8'))
                    flag = 0
                elif data != pwd_hamc or os.path.isfile('./account/' + user + '.txt'):
                    ssl_client_socket.send("登陆失败，用户名或密码不正确！\n请输入账号：".encode('utf-8'))
                    
                    # 迭代
                    for i in range(0, 4):
                        get_user_pwd()
                        if data == pwd_hamc and os.path.isfile('./account/' + user + '.txt'):
                            ssl_client_socket.send((user + "登陆成功！").encode('utf-8'))
                            flag = 0
                            break
                        elif data != pwd_hamc or os.path.isfile('./account/' + user + '.txt'):
                            if i < 3:
                                ssl_client_socket.send("登陆失败，用户名或密码不正确！\n请输入账号：".encode('utf-8'))
                            elif i == 3:
                                ssl_client_socket.send("登陆失败，用户名或密码不正确！\n登录次数已达5次，请下辈子在登录！".encode('utf-8'))
                                flag = 0
        
        elif choice == '0':  # 注册
            # 请求用户名
            ssl_client_socket.send("请输入用户名：".encode('utf-8'))
            
            # 接收客户端消息
            client_message = ssl_client_socket.recv(1024)  
            new_user = client_message.decode('utf-8')    
            print(new_user)

            # 检测用户名是否冲突
            if os.path.isfile('./account/' + new_user + '.txt'):
                ssl_client_socket.send("该用户名已存在！".encode('utf-8'))
                continue

            # 生成时间戳盐值
            salt = str(time.time())

            with open('./account/salt/' + new_user + '.txt', 'a', encoding='utf-8') as f:
                f.write(salt)

            # 请求密码
            ssl_client_socket.send("请输入密码：".encode('utf-8'))

            # 接收客户端消息
            client_message = ssl_client_socket.recv(1024)
            new_pwd = client_message.decode('utf-8')       
            print(new_pwd)

            # 获得加密后的密码
            new_user_md5 = md5_encrypt(new_user, salt)
            new_pwd_hamc = hamc_encrypt(new_pwd, new_user_md5)

            with open('./account/' + new_user + '.txt', 'a', encoding='utf-8') as f:
                f.write(new_pwd_hamc)
