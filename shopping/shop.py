#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author aliex-hrg.json
import os,sys,json
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

goods_list = {
    "1":{"icar":280000},
    "2":{"ipad":6888},
    "3":{"iphone":5888},
    "4":{"mihone":1999},
    "5":{"mi fan":19},
    "6":{"hong mi":999},
    "7":{"hat":9},
    "8":{"pen":7},
    "9":{"wrap":38}
}
curr_user = '' #当前用户
goods = []  #购物车列表
def print_goodslist():  #打印商品列表
    print("Supermarket Goods List:")
    print("\t%-7s%-10s%-10s" %("商品号","商品名","价格"))
    for i in goods_list:
        for j in goods_list[i]:
            print("\t%-10s%-13s%-13s"%(i,j,goods_list[i][j]),end='\n')

def showcar(data):
    print("你的购物车列表：")
    sum = 0
    for i in data:
        for j in i:
            print("商品名：%-10s  价格：%s元" % (j, i[j]))
            sum += i[j]
    print("\t\t\t\t合计：%s元" % sum)

def auth(data):   #购物车装饰器，实现认证用户功能
        def out_wrapper(func):
            def wrapper(*args,**kwargs):
                if curr_user == '':  # "判断是否已经登录"
                    username = input("Enter you username:").strip()
                    passwd = input("Enter you password:").strip()
                    with open(BASE_DIR + '/accounts/userlist.json','r',encoding='utf8') as f:  #首先从用户列表中查找是否存在该用户
                        if username in f.read():
                            with open(BASE_DIR + '/accounts/'+username+'.json', 'r') as f:
                                user = json.loads(f.read())
                            if username == user["username"] and passwd == user["password"]:
                                func(*args, **kwargs)
                                return username  #返回登录用户
                            else:print("password is wrong,exit");exit(2)
                        else:print("user is not exest,exit");exit(1)
                else:
                    func(*args, **kwargs)
            return wrapper
        return out_wrapper

@auth(curr_user)
def shopcar(name):
    goods.append(name)
def man_shop():
    while True:
        print_goodslist()
        choise = input("请选择你要购买的商品号（按q退出）：").strip()
        if choise and choise in goods_list:
            global curr_user #定义为全局变量，目的用户输入一次账号就记住了
            curr_user = shopcar(goods_list[choise])
            if curr_user:print("加入购物车成功")
            step = input("继续购物按1，去购物车结算按2:")
            if step == "2":
                showcar(goods)
                step2 = input("继续结算按1，取消按2：")
                if step2 == "2":
                    pass
                    break
        elif choise == 'q':break
        else:
            print("你选择的商品不存在，请重新选择:")



