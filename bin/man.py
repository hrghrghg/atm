#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author aliex-hrg.json

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
from atm import atm
from shopping import shop
while True:
    print("ATM + 购物车功能小程序")
    print("\t1.逛商场")
    print("\t2.ATM管理")
    choise = input("选择进入(q退出程序)>>:").strip()
    if choise == "1":
        shop.man_shop()
    elif choise == "2":
        atm.man_atm()
    elif choise == "q":
        exit(0)
