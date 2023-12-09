# Identity-Authentication-System
大三课程网络安全技术课程实践：身份认证系统

# 技术路线
![image](https://github.com/WaterBoyBia/Identity-Authentication-System/assets/109199725/5669de4a-406e-4175-bf62-ae40c4ba8250)

# 安全分析
①	服务器和客户端使用SSL连接，提供了加密和身份验证，防止数据被窃听和伪造，防止中间人攻击。

②	在输入密码时限制密码不能为空，且登录次数限制为5次。

③	将数据和网页文件分开存储，防止两个资产同时被攻击。

④	注册时检测用户名是否冲突

⑤	密码加密：将账号加入时间戳盐值后用md5加密获得散列值作为HMAC的密钥，使用HMAC对密码进行加密，digestmod模式选择为 hashlib.sha1，返回的散列值数据的长度为40位。该方法一定程度上防止了散列碰撞，且防止攻击者使用数据字典进行直接匹配。

![image](https://github.com/WaterBoyBia/Identity-Authentication-System/assets/109199725/2840a1ad-1408-4b82-bc30-1af59b8e69e1)

# 缺陷分析
①	没有考虑可能出现的web攻击或xss攻击。

②	密钥的生成过于简单。

③	没有第三方机构来证明用OPENSSL生成的服务器证书和私钥有正确性和合法性。

