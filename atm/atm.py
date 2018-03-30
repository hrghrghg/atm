#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author aliex-hrg.json

atm_menu_show = [
    "1.查询",
    "2.添加",
    "3.删除",
    "4.设置额度",
    "5.冻结余额",
    "6.每月还款"
]
def select():
    pass
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

man_atm()