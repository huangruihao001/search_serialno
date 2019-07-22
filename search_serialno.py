import re
import os
import requests

def get_code_html(serialno):
    # 传入锁号，获得授权码的html
    # 登录地址
    post_addr = "https://192.168.0.128/crm/product/authcode_search.php"

    # 构造头部信息
    post_header = {
        'Host': '192.168.0.128',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://192.168.0.128/crm/index.php',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '47',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=6dc605dee2ed74013e3e8402c2a42fa0',
        'Upgrade-Insecure-Requests': '1'
    }

    # 构造登录数据
    post_data = {
        'username': 'zhubing',
        'password': '123456',
        's_db': '',
        'x': '23',
        'y': '10',
        'serialno': serialno,
        'Button': '%C8%B7%C8%CF'
    }
    # 发送post请求登录网页
    z = requests.post(post_addr, data=post_data, headers=post_header, verify=False)
    z_gbk = z.content.decode('gbk')

    return z_gbk


def get_code_html_login():
    # 传入锁号，获得授权码的html
    # 登录地址
    post_addr = "https://192.168.0.128/crm/check.php"

    # 构造头部信息
    post_header = {
        'Host': '192.168.0.128',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://192.168.0.128/crm/index.php',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '47',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=6dc605dee2ed74013e3e8402c2a42fa0',
        'Upgrade-Insecure-Requests': '1'
    }

    # 构造登录数据
    post_data = {
        'username': 'zhubing',
        'password': '12345',
        's_db': '',
        'x': '23',
        'y': '10',
    }
    # 发送post请求登录网页
    z = requests.post(post_addr, data=post_data, headers=post_header, verify=False)

    return z.content.decode('gbk')


def get_code(serialno):
    # 读取授权码
    try:
        pattern = re.compile(r'(?<=<br>).*?(?=</body>)')
        html = get_code_html(serialno)
        result = pattern.findall(html)
        result = str(result)
        result = result.replace("br", "\n")
        result = result.replace("<", "")
        result = result.replace(">", "")
        result = result.replace("['", "")
        result = result.replace("']", "")
    except:
        return False
    if result == "[]":
        return False
    else:
        return result

def get_serialno(path):
    f = open(path)             # 返回一个文件对象
    serialno_list = []
    line = f.readline()             # 调用文件的 readline()方法
    while line:
        line_content = line.replace("\n", "")
        serialno_list.append(line_content)
        line = f.readline()
    f.close()
    return serialno_list

def write_serialnoCode(serialno_line):
    # 将查询到的授权码写入txt中
    for serialnoNum in serialno_line:
        serialnoCode = get_code(serialnoNum)
        if serialnoCode is False:
            print(serialnoNum + "查询授权码失败")
            text_create(serialnoNum + "查询授权码失败", '')
        else:
            print(serialnoCode)
            text_create(serialnoNum, serialnoCode)


def text_create(name, msg):
    # 创建一个txt文件，文件名为mytxtfile,并向文件写入msg
    desktop_path = "./授权码/"  # 新创建的txt文件的存放路径
    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档
    file = open(full_path, 'w')
    file.write(msg)   #msg也就是下面的Hello world!
    # file.close()


if __name__ == '__main__':
    serialno_line = get_serialno('待查询锁号.txt') # 读取txt中填写的锁号
    try:
        os.makedirs("./授权码")
    except:
        pass
    print(serialno_line)
    get_code_html_login() # 登录查询系统
    write_serialnoCode(serialno_line) # 将查询到的授权码写入txt中
