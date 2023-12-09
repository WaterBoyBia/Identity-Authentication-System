import socket
import ssl

# 创建 socket 对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 服务器地址和端口
server_address = ('localhost', 12345)

# 创建SSL包装的socket
ssl_client_socket = ssl.wrap_socket(client_socket, keyfile=None, certfile=None, server_side=False, ca_certs="server-cert.pem")

# 连接服务器
ssl_client_socket.connect(server_address)

while True:
    # 接收服务器消息
    server_message = ssl_client_socket.recv(1024)
    print(server_message.decode('utf-8'))

    # 用户输入消息
    client_message = input("(输入'client exit'退出)：")    
    if client_message == 'client exit':
        break  # 退出循环
    
    # 发送消息给服务器
    ssl_client_socket.send(client_message.encode('utf-8'))

# 关闭连接
client_socket.close()
