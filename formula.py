#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 17.01.2013

@author: adrianus
'''

# http://en.wikipedia.org/wiki/List_of_logic_symbols
# →, ¬, ∧, ∨, ⊥, ⊤, ⊢, ⊨


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
        formula = formula.replace(u'AND', u'∧')
        formula = formula.replace(u'OR', u'∨')
        formula = formula.replace(u'NOT', u'¬')
        formula = formula.replace(u'IMPL', u'→')
        formula = formula.replace(u'TOP', u'⊤')
        formula = formula.replace(u'BOTTOM', u'⊥')
        
        # TODO
        #formula = formula.replace(u'', u'⊢')
        #formula = formula.replace(u'', u'⊨')
        print 'formula:', formula
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
