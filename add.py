#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests, json
import datetime
from httpsig.requests_auth import HTTPSignatureAuth
import sys

import configparser


config = configparser.ConfigParser()
config.read("config.ini")


def add_host(hostname, ip, node):
    url = config['DEFAULT']['Url'] + '/api/v1/assets/assets/' #地址根据实际情况填写
    # web页面可以查到各种ID信息
    data = {
        'hostname': hostname, #主机名
        'ip': ip, #IP地址
        'platform': 'Linux', #操作系统
        'protocols': 'ssh/22', 
        #'nodes': ['----'], #资产节点id
        'nodes': [node], #资产节点id（）
        'is_active': True,  #是否激活
        'comment': "脚本自动化添加"  #备注
    }
    response = requests.post(url, auth=auth, headers=headers, data=data)
    print(response.text)
    #创建成功后返回主机id
    return json.loads(response.text)['id']


#需要先创建好，key_id 和secret根据实际情况填写
auth = HTTPSignatureAuth(key_id=config['DEFAULT']['AccessKeyID'], secret=config['DEFAULT']['AccessKeySecret'],
                         algorithm='hmac-sha256', headers=['(request-target)', 'accept', 'date'])
gmt_form = '%a, %d %b %Y %H:%M:%S GMT'
headers = {
    'Accept': 'application/json',
    'X-JMS-ORG': '00000000-0000-0000-0000-000000000002',
    'Date': datetime.datetime.utcnow().strftime(gmt_form)
}

if __name__ == '__main__':
    add_host(sys.argv[1], sys.argv[2], sys.argv[3]) #对应 def add_host(hostname, ip, node):