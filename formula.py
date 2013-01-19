#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 17.01.2013

@author: adrianus
'''

# http://en.wikipedia.org/wiki/List_of_logic_symbols
import re

class Formula(object):
    '''
    Represents a formula.
    '''
    
    def __init__(self, formula):
        '''
        Constructor
        '''
        self.formula = self.clean_up(formula)
        self.nnf = ''
        self.cnf = ''
    
    def clean_up(self, formula):
        substitutes = {u'0': u'\u2080', u'1': u'\u2081', u'2': u'\u2082', u'3': u'\u2083', u'4': u'\u2084',
                       u'5': u'\u2085', u'6': u'\u2086', u'7': u'\u2087', u'8': u'\u2088', u'9': u'\u2089',
                       u'AND': u'\u2227', u'OR': u'\u2228', u'NOT': u'\u00AC', u'IMPL': u'\u2192',
                       u'TOP': u'\u22A4', u'BOTTOM': u'\u22A5'}

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

        # checking for propositions
        #raise FormulaInvalidError('')

        # checking for conjunctions
        #raise FormulaInvalidError('')
        
        return formula
        
        
    def to_nnf(self, formula):
        # TODO implement
        return self.nnf
        
    def to_cnf(self, formula):
        # TODO implement
        return self.cnf
        
    def export_latex(self):
        # TODO implement
        formula = formula = self.formula
        formula = formula.replace(u'p', u'p_')
        
        formula = formula.replace(u'∧', u'\\wedge')
        formula = formula.replace(u'∨', u'\\vee')
        formula = formula.replace(u'¬', u'\\neg')
        formula = formula.replace(u'↔', u'\\leftrightarrow')
        formula = formula.replace(u'→', u'\\rightarrow')
        formula = formula.replace(u'⊤', u'\\top')
        formula = formula.replace(u'⊥', u'\\bot')
        
        return formula

### exceptions ###
    
class FormulaInvalidError(Exception):
    def __init__(self, arg):
        self.value = arg
