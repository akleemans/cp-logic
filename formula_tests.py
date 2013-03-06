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
    
    def test_invalidFormula_connectives1(self):
        string = 'p0 OR p1 IMPL p2 AND'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Connectives not matching in: " + string)
        
    def test_invalidFormula_connectives2(self):
        string = 'AND'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("No propositions for AND-clause in: " + string)
        
    def test_invalidFormula_propositions(self):
        string = 'p0 OR p1 IMPL p2 p1'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Propositions without connectives not allowed in: " + string)
    
    def test_invalidFormula_negation1(self):
        string = 'p0 OR NOT'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("No proposition for NOT in: " + string)
        
    def test_invalidFormula_negation2(self):
        string = 'p0 OR (p1 AND NOT)'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Missing proposition for NOT in: " + string)
        
    def test_invalidFormula_negation3(self):
        string = 'p0 NOT OR p2'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Missing proposition for NOT in: " + string)
        
    def test_invalidFormula_brackets1(self):
        string = '(p1 IMPL p2'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Closing bracket missing in: " + string)
        
    def test_invalidFormula_brackets2(self):
        string = '(p0))'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Too much closing brackets in: " + string)

    def test_invalidFormula_brackets3(self):
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
        
    def test_invalidFormula_empty1(self):
        string = ''
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Empty formula is not valid.")
        
    def test_invalidFormula_empty2(self):
        string = '()'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("() is an empty formula and not valid.")
        
    def test_validFormula1(self):
        string = 'p0 IMPL p1'
        formula = Formula(string)
        self.failUnless(isinstance(formula, Formula))
        
    def test_validFormula2(self):
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
        
    def test_formula_length3(self):
        string = 'p0 OR p1 IMPL p2 AND NOT p3'
        formula = Formula(string)
        self.failUnless(formula.length() == 8)
        
    def test_formula_length4(self):
        string = 'p0 OR p1 IMPL p2 AND p0'
        formula = Formula(string)
        self.failUnless(formula.length() == 6)
        
#    def test_pedantic(self):
#        string = 'p0 OR p1 IMPL p1 AND p2'
#        formula = Formula(string)
#        self.failUnless(formula.formula != formula.formula_pedantic)

#    def test_nnf1(self):
#        string = 'p0 IMPL p1'
#        formula = Formula(string)
#        self.failUnless(formula.length() == 4)
        
if __name__ == "__main__":
    unittest.main()
