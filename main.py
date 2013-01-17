#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 17.01.2013

@author: adrianus
'''

import time
from formula import *

if __name__ == '__main__':

    # some test objects
    f = Formula(u'p0 AND (NOT p1 OR p2)')
    #f.to_nnf()
    print f.export_latex()
