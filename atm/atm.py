#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author aliex-hrg.json
import os,sys,json
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
atm_menu_show = [
    "1.查询",
    "2.添加",
    "3.删除",
    "4.设置额度",
    "5.冻结余额",
    "6.每月还款"
]
def select():
    print("in the select")
def add():
    pass
def remove():
    pass
def setbalance():
    pass
def frozen():
    pass
def repayment():
    pass

def api_payment(user,num):  #让购物车调用的扣款接口，参数扣款的用户和扣款金额
    info = getuserinfo(user)
    if info["balance"] - int(num) < -15000:
        print("信用卡透支，无法购买")
    else:
        info["balance"] -= int(num)
    changeuserinfo(user,info)
def getuserinfo(user):   #获取指定用户的json信息，返回整个文件
    with open(BASE_DIR + '/accounts/userlist.json','r',encoding='utf8') as f:
        if user and user in f.read():
            with open(BASE_DIR + '/accounts/'+user+'.json','r',encoding='utf8') as f1:
                temp = json.loads(f1.read())
            return temp
def changeuserinfo(user,changeinfo):   #修改用户信息接口，changeinfo为整个用户信息文件内容
    with open(BASE_DIR + '/accounts/userlist.json', 'r', encoding='utf8') as f:
        if user and user in f.read():
            with open(BASE_DIR + '/accounts/' + user + '.json', 'w', encoding='utf8') as f1:
                f1.write(json.dumps(changeinfo))

atm_menu = {
    "1":select,
    "2":add,
    "3":remove,
    "4":setbalance,
    "5":frozen,
    "6":repayment
}

def man_atm():
    print("ATM 功能列表：")
    for i in atm_menu_show:
        print("\t"+i)
    while True:
        choise = input("请选择功能：")
        atm_menu[choise]()

#man_atm()
