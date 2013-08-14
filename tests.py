#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Tests for the formula class.

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
        
    def test_invalidFormula_empty3(self):
        string = '(())'
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
        
    ### length()
    
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
        
    def test_formula_length5(self):
        string = 'p0 OR p1 OR p2 OR p3 OR p4 OR p5'
        formula = Formula(string)
        self.failUnless(formula.length() == 11)
        
    def test_formula_length6(self):
        string = 'p0 OR p0 OR p0 OR p0 OR p0'
        formula = Formula(string)
        self.failUnless(formula.length() == 5)
    
    ### pedantic()
    
    def test_pedantic1(self):
        string = 'p0 OR p1 IMPL p1 AND p2'
        formula = Formula(string)
        self.failUnless(formula.formula_pedantic == u'( p₀ ∨ p₁ ) → ( p₁ ∧ p₂ )')
        
    def test_pedantic2(self):
        string = 'p0 AND p1 AND p2'
        formula = Formula(string)
        self.failUnless(formula.formula_pedantic == u'( p₀ ∧ p₁ ) ∧ p₂')
        
    def test_pedantic3(self):
        string = 'p0 AND p1 AND p2 AND p3'
        formula = Formula(string)
        self.failUnless(formula.formula_pedantic == u'( ( p₀ ∧ p₁ ) ∧ p₂ ) ∧ p₃')
        
    def test_pedantic4(self):
        string = 'p0 OR p1 OR p2 OR p3 OR p4 OR p5'
        formula = Formula(string)
        self.failUnless(formula.formula_pedantic == u'( ( ( ( p₀ ∨ p₁ ) ∨ p₂ ) ∨ p₃ ) ∨ p₄ ) ∨ p₅')
        
    def test_pedantic5(self):
        string = 'p0 OR p1 OR p2 OR p3 OR p4 OR p5 OR p6 OR p7 OR p8 OR p9 OR p10'
        formula = Formula(string)
        self.failUnless(formula.formula_pedantic == u'( ( ( ( ( ( ( ( ( p₀ ∨ p₁ ) ∨ p₂ ) ∨ p₃ ) ∨ p₄ ) ∨ p₅ ) ∨ p₆ ) ∨ p₇ ) ∨ p₈ ) ∨ p₉ ) ∨ p₁₀')
    
    def test_pedantic6(self):
        string = 'p0 OR p1 OR (p2 AND p3 IMPL p1)'
        formula = Formula(string)
        self.failUnless(formula.formula_pedantic == u'( p₀ ∨ p₁ ) ∨ ( ( p₂ ∧ p₃ ) → p₁ )')
        
    def test_pedantic7(self):
        string = 'p0 AND p1 IMPL p2 AND p3 IMPL p4'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail('More than one implication not allowed.')
        
    def test_pedantic8(self):
        string = 'p0 AND p1 OR p2'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail('Mixed ANDs and ORs are not allowed.')
        
    def test_pedantic9(self):
        string = 'p0 OR p1 OR (p2 AND p3) OR p4'
        formula = Formula(string)
        self.failUnless(formula.formula_pedantic == u'( ( p₀ ∨ p₁ ) ∨ ( p₂ ∧ p₃ ) ) ∨ p₄')
        
    def test_pedantic10(self):
        string = 'p0 OR NOT p1 OR NOT p2 IMPL p0 AND p1 AND p2'
        formula = Formula(string)
        self.failUnless(formula.formula_pedantic == u'( ( p₀ ∨ ¬ p₁ ) ∨ ¬ p₂ ) → ( ( p₀ ∧ p₁ ) ∧ p₂ )')
        
    def test_pedantic11(self):
        string = 'p0 OR (p1 AND p2 AND p3) IMPL (p5 AND (p6 OR p7) AND p8)'
        formula = Formula(string)
        self.failUnless(formula.formula_pedantic == u'( p₀ ∨ ( ( p₁ ∧ p₂ ) ∧ p₃ ) ) → ( ( p₅ ∧ ( p₆ ∨ p₇ ) ) ∧ p₈ )')
    
    ### nnf()
    
    def test_nnf1(self):
        string = 'p0'
        formula = Formula(string)
        self.failUnless(formula.formula_nnf == u'p₀')
        
    def test_nnf2(self):
        string = 'p0 IMPL p1'
        formula = Formula(string)
        self.failUnless(formula.formula_nnf == u'¬ p₀ ∨ p₁')
        
    def test_nnf3(self):
        string = 'p0 AND p1 IMPL p2'
        formula = Formula(string)
        self.failUnless(formula.formula_nnf == u'( ¬ p₀ ∨ ¬ p₁ ) ∨ p₂')
        
    def test_nnf4(self):
        string = 'p0 AND (p1 OR p2) IMPL p2'
        formula = Formula(string)
        self.failUnless(formula.formula_nnf == u'( ¬ p₀ ∨ ( ¬ p₁ ∧ ¬ p₂ ) ) ∨ p₂')
        
    def test_nnf5(self):
        string = 'p0 IMPL NOT (p0 AND p1)'
        formula = Formula(string)
        self.failUnless(formula.formula_nnf == u'¬ p₀ ∨ ( ¬ p₀ ∨ ¬ p₁ )')
        
    def test_nnf6(self):
        string = 'NOT (p0 AND p1)'
        formula = Formula(string)
        self.failUnless(formula.formula_nnf == u'( ¬ p₀ ∨ ¬ p₁ )')
        
    def test_nnf7(self):
        string = 'NOT ((p0 AND p1) OR (p2 OR p3))'
        formula = Formula(string)
        self.failUnless(formula.formula_nnf == u'( ( ¬ p₀ ∨ ¬ p₁ ) ∧ ( ¬ p₂ ∧ ¬ p₃ ) )')
        
    def test_nnf8(self):
        string = 'NOT NOT p0'
        formula = Formula(string)
        self.failUnless(formula.formula_nnf == u'p₀')
        
    def test_nnf9(self):
        string = 'NOT NOT NOT (p0 AND NOT p1)'
        formula = Formula(string)
        self.failUnless(formula.formula_nnf == u'( ¬ p₀ ∨ p₁ )')
        
    def test_nnf10(self):
        string = 'NOT ((p0 AND p1) OR (p2 OR p3))'
        formula = Formula(string)
        self.failUnless(formula.formula_nnf == u'( ( ¬ p₀ ∨ ¬ p₁ ) ∧ ( ¬ p₂ ∧ ¬ p₃ ) )')
        
    def test_nnf11(self):
        string = 'NOT (p0 AND NOT (p1 AND NOT (NOT p2 OR NOT p3)))'
        formula = Formula(string)
        self.failUnless(formula.formula_nnf == u'( ¬ p₀ ∨ ( p₁ ∧ ( p₂ ∧ p₃ ) ) )')
        
    ### sufo()
    
    def test_sufo1(self):
        string = 'p0'
        formula = Formula(string)
        self.failUnless(formula.sufo() == [u'p₀'])
        
    def test_sufo2(self):
        string = 'p0 AND p1'
        formula = Formula(string)
        self.failUnless(formula.sufo() == [u'p₀', u'p₁', u'p₀ ∧ p₁'])
        
    def test_sufo3(self):
        string = 'NOT p0 IMPL p1'
        formula = Formula(string)
        self.failUnless(formula.sufo() == [u'p₀', u'p₁', u'¬ p₀', u'¬ p₀ → p₁'])
        
    def test_sufo4(self):
        string = 'NOT ((p0 AND p1) OR (p2 OR p3))'
        formula = Formula(string)
        self.failUnless(formula.sufo() == [u'p₀', u'p₁', u'p₂', u'p₃', u'( p₀ ∧ p₁ )', u'( p₂ ∨ p₃ )', u'( ( p₀ ∧ p₁ ) ∨ ( p₂ ∨ p₃ ) )', u'¬ ( ( p₀ ∧ p₁ ) ∨ ( p₂ ∨ p₃ ) )'])

    def test_sufo5(self):
        string = 'p0 AND (NOT p1 OR p2)'
        formula = Formula(string)
        self.failUnless(formula.sufo() == [u'p₀', u'p₁', u'p₂', u'¬ p₁', u'( ¬ p₁ ∨ p₂ )', u'p₀ ∧ ( ¬ p₁ ∨ p₂ )'])

    def test_sufo6(self):
        string = 'p0 AND NOT (p1 AND NOT (p2 AND NOT p3))'
        formula = Formula(string)
        self.failUnless(formula.sufo() == [u'p₀', u'p₁', u'p₂', u'p₃', u'¬ p₃', u'( p₂ ∧ ¬ p₃ )', u'¬ ( p₂ ∧ ¬ p₃ )', u'( p₁ ∧ ¬ ( p₂ ∧ ¬ p₃ ) )', u'¬ ( p₁ ∧ ¬ ( p₂ ∧ ¬ p₃ ) )', u'p₀ ∧ ¬ ( p₁ ∧ ¬ ( p₂ ∧ ¬ p₃ ) )'])


if __name__ == "__main__":
    unittest.main()