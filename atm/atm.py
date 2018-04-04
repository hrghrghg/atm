#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author aliex-hrg.json
import os,sys,json,time
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
atm_menu_show = [
    "1.查询",
    "2.添加",
    "3.注销",
    "4.转账",
    "5.提现",
    "6.冻结解冻",
    "7.每月还款",
    "8.打印账单"
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
        info = {'username':username,'password':passwd,'balance':balance,'limit':limit,'frozon':False}
        changeuserinfo(username,info)
        log = "添加用户"+username
    else:
        print("添加的用户已经存在")
        log = "添加用户失败，用户已经存在"
    writeatmlog(log)
def remove():
    username = input("请输入你要注销的用户：").strip()
    if os.path.isfile(BASE_DIR+'/accounts/'+username+'.json'):
        os.remove(BASE_DIR+'/accounts/'+username+'.json')
        print("注销用户%s成功" %username)
        writeatmlog("注销用户%s成功" %username)
    else:
        print("你输入的用户不存在")
        writeatmlog("你输入的用户%s不存在" %username)
    if os.path.isfile(BASE_DIR + '/logs/' + username + '.log'):
        os.remove(BASE_DIR + '/logs/' + username + '.log')
        print("删除用户%s的日志成功" %username)
        writeatmlog("删除用户%s的日志成功" %username)
def transfer():
    print("\t\t转账系统")
    fromusername = input("请输入转账人用户名：").strip()
    passwd = input("请输入转账人密码：").strip()
    fromuser = getuserinfo(fromusername)
    if fromuser["frozon"]:
        print("%s用户已经被冻结"%fromusername)
        writeatmlog("%s用户已经被冻结,不支持转出"%fromusername)
        return "fail"
    if passwd == fromuser["password"]:
        print("登录成功，%s，欢迎你" %fromusername)
        tousername = input("请输入转入方账号：").strip()
        touser = getuserinfo(tousername)
        if touser["frozon"]:
            print("%s用户已经被冻结" %tousername)
            writeatmlog("%s用户已经被冻结,不支持转入" %tousername)
            return "fail"
        tonum = int(input("请输入转入金额："))
        if fromuser["balance"] - tonum < - fromuser["limit"]:
            print("你的信用额度不够，少转点。")
            writeatmlog("%s转账给%s失败，可用额度不够" %(fromusername,tousername))
            return "fail"
        else:
            fromuser["balance"] -= tonum
            touser["balance"] += tonum
            changeuserinfo(tousername,touser)
            changeuserinfo(fromusername,fromuser)
            writeatmlog("%s用户转账给%s用户%s元成功" %(fromusername,tousername,tonum))
            print("转入成功")
    else:
        print("密码不对")
def withdraw():
    print("\t\t提现系统")
    username = input("请输入用户名：").strip()
    passwd = input("请输入密码：").strip()
    fromuser = getuserinfo(username)
    if fromuser["frozon"]:
        print("%s用户已经被冻结"%username)
        writeatmlog("%s用户已经被冻结,不支持提现"%username)
        return "fail"
    if passwd == fromuser["password"]:
        print("登录成功，%s，欢迎你" %username)
        bill = int(input("请输入提现金额："))
        if fromuser["balance"] - bill < - fromuser["limit"]:
            print("你的提现额度超过信用额度了。")
            writeatmlog("%s提现%s元失败，可用额度不够" %(username,bill))
        else:
            fromuser["balance"] = fromuser["balance"] - bill - bill*5/100
            changeuserinfo(username,fromuser)
            writeatmlog("%s提现%s元成功" %(username,bill))
            print("提现成功")
def frozen():
    print("\t\t冻结系统")
    username = input("请输入要操作的用户名：").strip()
    act = input("冻结按1，解冻按2").strip()
    fromuser = getuserinfo(username)
    if act == "1":
        fromuser["frozon"] = True
        log = "冻结%s用户成功" %username
    elif act == "2":
        fromuser["frozon"] = False
        log = "解冻%s用户成功" %username
    else:
        print("输入有误")
        return "fail"
    changeuserinfo(username,fromuser)
    print(log)
    writeatmlog(log)
def repayment():
    print("\t\t还款系统")
    username = input("请输入用户名：").strip()
    passwd = input("请输入密码：").strip()
    fromuser = getuserinfo(username)
    if passwd == fromuser["password"]:
        print("登录成功，%s，欢迎你" %username)
        balance = fromuser["balance"]
        if balance > 0:
            print("你目前的余额为%s元,不需要还款" %balance)
            return "do not repayment"
        else:
            print("你目前的余额为%s元,需要还款%s元" %(balance,abs(balance)))
        bill = int(input("请输入要还款的金额："))
        fromuser["balance"] = fromuser["balance"] + bill
        changeuserinfo(username,fromuser)
        writeatmlog("%s还款%s元成功" %(username,bill))
        print("还款成功")
def printbill():
    print("\t\t打印账单系统")
    username = input("请输入用户名：").strip()
    passwd = input("请输入密码：").strip()
    fromuser = getuserinfo(username)
    if passwd == fromuser["password"]:
        print("登录成功，%s，欢迎你" %username)
    date1 = input("输入打印账单开始日期,格式:2018-04-03 12:00:00>>>:")
    date2 = input("输入打印账单结束日期,格式:2018-04-03 20:00:00>>>:")
    with open(BASE_DIR+'/logs/'+username+'.log','r',encoding='utf8') as f:
        for i in f:
            if i[:19] >= date1 and i[:19] < date2:
                print(i.strip())
    writeatmlog("打印用户%s的账单%s到%s" %(username,date1,date2))
def api_payment(user,num):  #让购物车调用的扣款接口，参数扣款的用户和扣款金额
    info = getuserinfo(user)
    if info["frozon"]:
        print("%s用户已经被冻结"%user)
        writeatmlog("%s用户已经被冻结,支付失败"%user)
        return "fail"
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
    "4":transfer,
    "5":withdraw,
    "6":frozen,
    "7":repayment,
    "8":printbill
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
