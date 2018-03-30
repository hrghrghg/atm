#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author aliex-hrg.json

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
from atm import atm
from shopping import shop

shop.man_shop()