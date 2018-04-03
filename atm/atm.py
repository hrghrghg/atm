#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author aliex-hrg.json
import os,sys,json,time
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
    user = input("请输入要查询的用户>>:")
    if os.path.isfile(BASE_DIR+'\\accounts\\'+user+'.json'):
        print(getuserinfo(user))
        log = "查询到此用户："+user
    else:
        print("查无此用户")
        log = "查询"+user+"用户，没有结果"
    writeatmlog(log)
def add():
    username = input("请输入用户名：")
    if not os.path.isfile(BASE_DIR + '/accounts/' + username + '.json'):
        passwd = input("请输入密码：")
        balance = int(input("请输入存款金额："))
        limit = int(input("请设置信用额度："))
        info = {'username':username,'password':passwd,'balance':balance,'limit':limit}
        changeuserinfo(username,info)
        log = "添加用户"+username
    else:
        print("添加的用户已经存在")
        log = "添加用户失败，用户已经存在"
    writeatmlog(log)
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
    if info["balance"] - int(num) < - info["limit"]:
        print("超过信用卡透支额度，无法购买")
        writeatmlog("%s购物支付失败" %user)
        return "fail"
    else:
        info["balance"] -= int(num)
    changeuserinfo(user,info)
    writeatmlog("%s用户购物支付成功" %user)
    return info["balance"]
def getuserinfo(user):   #获取指定用户的json信息，返回整个文件
    if os.path.isfile(BASE_DIR + '/accounts/'+user+'.json'):
        with open(BASE_DIR + '/accounts/'+user+'.json','r',encoding='utf8') as f1:
            temp = json.loads(f1.read())
        return temp
    else:
        print("此用户不存在！请确认输入")
def changeuserinfo(user,changeinfo):   #修改用户信息接口，changeinfo为整个用户信息文件内容
        with open(BASE_DIR + '/accounts/' + user + '.json', 'w', encoding='utf8') as f1:
            f1.write(json.dumps(changeinfo))
def writeatmlog(lines):  #lines为要写的日志
    with open(BASE_DIR + '/logs/atm.log','a',encoding='utf8') as f:
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        f.write("%s %s\n" %(curr_time,lines))

atm_menu = {
    "1":select,
    "2":add,
    "3":remove,
    "4":setbalance,
    "5":frozen,
    "6":repayment
}

def man_atm():
    while True:
        print("ATM 功能列表：")
        for i in atm_menu_show:
            print("\t" + i)
        choise = input("请选择功能,q返回上一层>>：")
        if choise == 'q':
            break
        elif choise and choise in atm_menu:
            atm_menu[choise]()

#man_atm()
