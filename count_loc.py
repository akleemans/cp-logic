#!/usr/bin/python
# -*- coding: ascii -*-
'''
Counts the LOC (lines of code) of python files in a directory.

@author: Adrianus Kleemans
@date: 2013
'''

import glob

count = []
functions = []
for f in glob.glob('*.py'):
    count.append(0)
    for line in open(f, 'r').readlines():
        if line.strip() != '':
            count[-1] += 1
        if line.strip().startswith('def') and not line.strip().startswith('def test'):
            functions.append(line.strip())
    print f, 'has', count[-1], 'lines of code.'
    
print 'Found', sum(count), 'lines of code in total.'

print 'Found', len(functions), 'functions.'
print functions
