#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 17.01.2013

@author: adrianus
'''

# http://en.wikipedia.org/wiki/List_of_logic_symbols
import re
import locale
import time

locale.setlocale(locale.LC_ALL, '')

class Formula(object):
    '''
    Represents a formula.
    '''
    
    
    def __init__(self, formula, name='_anon'):
        '''
        Constructor
        '''
        
        # static
        self.brackets = ['(', ')']
        
        self.NOT = u'\u00AC'
        self.AND = u'\u2227'
        self.OR = u'\u2228'
        self.IMPL = u'\u2192'
        self.conjunctions = [self.AND, self.OR, self.IMPL]
        
        self.TOP = u'\u22A4'
        self.BOTTOM = u'\u22A5'
        self.atomic_propositions = [self.TOP, self.BOTTOM]
        self.connectives = self.conjunctions + [self.NOT] + self.atomic_propositions #[u'\u2227', u'\u2228', u'\u00AC', u'\u2192', u'\u22A4', u'\u22A5']

        self.numbers = [u'\u2080', u'\u2081', u'\u2082', u'\u2083', u'\u2084', u'\u2085', u'\u2086', u'\u2087', u'\u2088', u'\u2089']
        
        # formula
        self.formula = self.clean_up(formula)
        self.name = name
        self.nnf = ''
        self.cnf = ''
    
    def clean_up(self, formula):
        substitutes = {u'0': u'\u2080', u'1': u'\u2081', u'2': u'\u2082', u'3': u'\u2083', u'4': u'\u2084',
                       u'5': u'\u2085', u'6': u'\u2086', u'7': u'\u2087', u'8': u'\u2088', u'9': u'\u2089',
                       u'AND': self.AND, u'OR': self.OR, u'NOT': self.NOT, u'IMPL': self.IMPL,
                       u'TOP': self.TOP, u'BOTTOM': self.BOTTOM}

        for a, b in substitutes.items():
            formula = formula.replace(a, b)

        # checking for brackets
        counter = 0
        for c in formula:
            if c == '(':
                counter += 1
            elif c == ')':
                counter -= 1
            if counter < 0:
                raise FormulaInvalidError('brackets in illegal order')
                
        if counter > 0:
            raise FormulaInvalidError('too many opening brackets')
        if counter < 0:
            raise FormulaInvalidError('too many closing brackets')
        
        # checking for illegal characters
        residue = re.sub(ur'([0-9p() \u2227\u2228\u00AC\u2192\u22A4\u22A5\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089]+)', '', formula)
        if len(residue) != 0:
            raise FormulaInvalidError('illegal characters: '+residue)
        
        # adding spaces
        f = ''
        conn = self.connectives
        for i in range(len(formula)):
            c = formula[i]
            f += c
            if c in conn or c in self.brackets:
                if i < len(formula)-1 and formula[i+1] != ' ':
                    f += ' '
            if c in self.numbers:
                if i < len(formula)-1 and formula[i+1] not in self.numbers and formula[i+1] != ' ':
                    f += ' '
        
        # checking for propositions
        parts = f.split()
        for part in parts:
            if part == 'p':
                raise FormulaInvalidError('propositions need an index')
        
        # checking for negations
        for i in range(len(parts)):
            part = parts[i]
            if part == self.NOT and i < len(parts)-1 and parts[i+1] == ')':
                        raise FormulaInvalidError('illegal negation')

        # checking for conjunctions
        for i in range(len(parts)):
            part = parts[i]
            if part in self.conjunctions:
                if i < len(parts)-1:
                    if parts[i+1] in self.conjunctions or parts[i+1] == ')':
                        raise FormulaInvalidError('illegal conjunction')
    
        return f
    
    def to_list(self, formula):
        return self.formula.split(' ') 
        
    def length(self):
        parts = self.to_list(self.nnf)
        count = []
        conn = self.connectives
        for part in parts:
            if (part not in conn and part in count) or part == '(' or part == ')':
                continue
            count.append(part)
        return len(count)
        
    def to_nnf(self):
        # TODO implement
        self.nnf = ''
        
    def to_cnf(self, formula):
        # TODO implement
        self.cnf = ''
        
    def latex(self):
        formula = self.formula
        substitutes = {u'\u2080': u'0', u'\u2081': u'1', u'\u2082': u'2', u'\u2083': u'3', u'\u2084': u'4',
                       u'\u2085': u'5', u'\u2086': u'6', u'\u2087': u'7', u'\u2088': u'8', u'\u2089': u'9',
                       self.AND: u'\\wedge', self.OR: u'\\vee', self.NOT: u'\\neg', self.IMPL: u'\\rightarrow',
                       self.TOP: u'\\top', self.BOTTOM: u'\\bot', u'p': u'p_'}

        for a, b in substitutes.items():
            formula = formula.replace(a, b)
        
        return formula
    
    def sat(self):
        # 1. to NNF
        #self.to_nnf()
        
        # 2. number of prop
        parts = self.to_list(self.formula)
        #print 'Parts: ', parts
        
        propositions = []
        for part in parts:
            if part not in (self.connectives + self.brackets):
                propositions.append(part)
        
        propositions = list(set(propositions))
        propositions.sort()
        #print 'Propositions:', propositions
        
        high = 2**len(propositions)
        print 'Found', len(propositions), 'distinct propositions =>', high, 'possibilities'
        
        # replace TOP and BOTTOM with t and f
        for i in range(len(parts)):
            if parts[i] == self.TOP: parts[i] = 't'
            if parts[i] == self.BOTTOM: parts[i] = 'f'
        
        # 3. resolve
        t1 = time.time()
        subst = {'1': 't', '0': 'f'}
        for i in range(high):
            if (time.time() - t1) > 5:
                raise TimeOutError('calculation aborted after ' + str(round(time.time() - t1, 3)) + ' seconds')
            formula = list(parts) # deep copy
            binary = ('{0:0' + str(len(propositions)) + 'b}').format(i) # einschl. Index
            
            # replace propositions with valuation i (represented as 'binary')
            for j in range(len(propositions)):
                formula = [subst[binary[j]] if x == propositions[j] else x for x in formula]
            
            # replace negations
            j = 0
            while j < len(formula):
                if formula[j] == self.NOT:
                    if formula[j+1] == 't':
                        formula[j+1] = 'f'
                        del formula[j]
                    elif formula[j+1] == 'f':
                        formula[j+1] = 't'
                        del formula[j]
                    else:
                        raise FormulaInvalidError('formula invalid/not in NNF')
                j += 1
            
            if self.resolve(formula):
                # prepare Valuation
                truth_values = [subst[x] for x in binary]
                valuation = []
                for i in range(len(propositions)):
                    valuation.append(propositions[i] + ' = ' + truth_values[i])
                
                return [True, valuation]
                
        return [False, []]
        
    def resolve(self, l):
        #print 'Resolving', ' '.join(x for x in l)
        while len(l) > 1:
            for i in range(len(l)):
                # resolve AND, OR
                if l[i] in self.conjunctions:
                    if l[i-1] in ['t', 'f'] and l[i+1] in ['t', 'f']:
                        new_value = ''
                        if l[i] == self.AND:
                            if l[i-1] == 't' and l[i+1] == 't': new_value = 't'
                            else: new_value = 'f'
                        elif l[i] == self.OR:
                            if l[i-1] == 't' or l[i+1] == 't': new_value = 't'
                            else: new_value = 'f'
                        else:
                            raise FormulaInvalidError('formula invalid/not in NNF')
                        
                        del l[i+1]
                        l[i] = new_value
                        del l[i-1]
                        break # start over

                # resolve brackets
                if i > 0 and i < len(l)-1 and l[i-1] == '(' and l[i+1] == ')':
                    del l[i+1]
                    del l[i-1]
                    break # start over
                
        return l == ['t']
        
### exceptions ###
    
class FormulaInvalidError(Exception):
    def __init__(self, arg):
        self.value = arg

class TimeOutError(Exception):
    def __init__(self, arg):
        self.value = arg
