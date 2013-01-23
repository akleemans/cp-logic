#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 23.01.2012

@author: adrianus
'''

import unittest
from formula import *

class FormulaTest(unittest.TestCase):

    def setUp(self):
        print 'Starting tests...'
    
    def test_invalidFormula_connectives(self):
        string = 'p0 OR p1 IMPL p2 AND'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Connectives not matching in: " + string)
        
        string = 'AND'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("No propositions for AND-clause in: " + string)
        
    def test_invalidFormula_propositions(self):
        string = 'p0 OR p1 IMPL p2 p1'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Propositions without connectives not allowed in: " + string)
    
    def test_invalidFormula_negation(self):
        string = 'p0 OR NOT'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("No proposition for NOT in: " + string)
        
        string = 'p0 OR (p1 AND NOT)'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Missing proposition for NOT in: " + string)
        
        string = 'p0 NOT OR p2'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Missing proposition for NOT in: " + string)
        
    def test_invalidFormula_brackets(self):
        string = '(p1 IMPL p2'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Closing bracket missing in: " + string)
        
        string = '(p0))'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Too much closing brackets in: " + string)
        
        string = ')(p0)('
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Brackets invalid in: " + string)
        
    def test_invalidFormula_implications1(self):
        string = 'p1 IMPL p2 IMPL p0'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Two implications on main level in: " + string)
        
    def test_invalidFormula_implications2(self):
        string = 'p2 AND (p1 IMPL p2 IMPL p3) OR p0'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Two implications on first nested level in: " + string)
        
    def test_invalidFormula_empty(self):
        string = ''
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Empty formula is not valid.")
        
        string = '()'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("() is an empty formula and not valid.")
        
    def test_validFormula(self):
        string = 'p0 IMPL p1'
        formula = Formula(string)
        self.failUnless(isinstance(formula, Formula))
        
        string = '((p0))'
        formula = Formula(string)
        self.failUnless(isinstance(formula, Formula))
    
    def test_formula_name(self):
        string = 'p0'
        formula = Formula(string, 'formula1')
        self.failUnless(formula.name == 'formula1')
        
    def test_formula_length1(self):
        string = 'p0'
        formula = Formula(string)
        self.failUnless(formula.length() == 1)
        
    def test_formula_length2(self):
        string = 'p0 OR p1 IMPL p2 AND p3'
        formula = Formula(string)
        self.failUnless(formula.length() == 7)
        
        string = 'p0 OR p1 IMPL p2 AND NOT p3'
        formula = Formula(string)
        self.failUnless(formula.length() == 8)
        
        string = 'p0 OR p1 IMPL p2 AND p0'
        formula = Formula(string)
        self.failUnless(formula.length() == 6)
        
if __name__ == "__main__":
    unittest.main()
