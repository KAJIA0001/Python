# from IPy import IP
# ip_s = input('IP:')
# ips = IP(ip_s)
# if len(ips):
#     print('net: %s'% ips.net()) # 输出网络地址
#     print('netmask: %s'% ips.netmask()) # 输出网络掩码地址
#     print('broadcast: %s'% ips.broadcast())# 输出网络广播地址
#     print('reverse address: %s'% ips.reverseNames()[0])# 输出地址反向解析
#     print('subnet: %s'% len(ips)) # 输出网络子网数
# else: # 为单个IP地址
#     print('reverse address: %s'% ips.reverseNames()[0])#输出IP反向解析

# print('hexadecimal: %s' % ips.strHex())# 输出十六进制地址
# print('binary ip: %s'% ips.strBin())#输出二进制地址
# print('iptype: %s'% ips.iptype())# 输出地址类型例如PRIVATE PUBLIC LOOPBACK等

# import dns.resolver
# domain = input('Please input an domain:')# 输入域名地址
# A = dns.resolver.query(domain,'A')# 指定查询类型为A记录
# for i in A.response.answer: # 通过reponse.answer方法获取查询回应信息
#     for j in i.items: # 遍历回应信息
#         print(j.address)

# import dns.resolver
# domain = input('Please input an domain:')# 输入域名地址
# MX = dns.resolver.query(domain,'MX')# 指定查询类型为MX记录
# for i in MX: # 遍历回应结果，输出MX记录的preference以及exchanger信息
#     print('MX preference = ',i.preference,'mail exchanger = ',i.exchange)

# import dns.resolver
# domain = input('Please input an domain:')# 输入域名地址
# ns = dns.resolver.query(domain,'NS')# 指定查询类型为NS记录
# for i in ns.response.answer: 
#     for j in i.items:
#         print(j.to_text())

# import dns.resolver
# domain = input('Please input an domain:')# 输入域名地址
# cname = dns.resolver.query(domain,'CNAME')# 指定查询类型为CNAME记录
# for i in cname.response.answer: 
#     for j in i.items:
#         print(j.to_text())

import dns.resolver
import os
import http.client


iplist = [] # 定义域名IP列表变量
appdomain = "www.baidu.com" #定义业务域名
def get_iplist(domain = ""): #域名解析函数解析成功ip将被追加到iplist
    try:
        A = dns.resolver.query(domain,'A') #解析A记录类型
    except Exception as e:
        print("dns resolver error:"+str(e))
        return
    for i in A.response.answer:
        for j in i.items:
            iplist.append(j) # 追加到iplist
    return True

def checkip(ip):
    checkurl = ip + ":"
    getcontent = ""
    http.client.socket.setdefaulttimeout(5)#定义http连接超时时间是5秒
    conn = http.client.HTTPConnection(checkurl)#创建http连接对象
    try:
        headers = {"Host":appdomain}
        conn.request("GET","/",headers)
        #发起URL请求，添加host主机头
        r = conn.getresponse()
        getcontent = r.read(15)# 获取UPL页面前15个字符，以便做可用性校验
    finally:
        if getcontent == "<!doctype html>":#监控URL页的内容一般是实现定义好的，比如"HTTP200"等
            print(ip + "[ok]")
        else:
            print(ip + "[Error]") #此处可以做告警程序，可以是邮件、短信通知
if __name__ == "__main__":
    if get_iplist(appdomain) and len(iplist) > 0:
        for ip in iplist:
            checkip(ip)
    else:
        print("dns resolver error.")