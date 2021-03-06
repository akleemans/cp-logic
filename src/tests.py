#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Tests for the formula class.

@author: adrianus
'''

import unittest
from formula import *
from tools import *

class Tests(unittest.TestCase):

    def setUp(self):
        print 'Starting tests...'
        self.tools = Tools()

    ### formula validation

    # connectives

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

    # propositions

    def test_invalidFormula_propositions1(self):
        string = 'p0 OR OR NOT p1'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Propositions without connectives not allowed in: " + string)

    def test_invalidFormula_propositions2(self):
        string = 'p0 OR p1 IMPL p2 p1'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Propositions without connectives not allowed in: " + string)

    def test_invalidFormula_propositions3(self):
        string = 'OR p0'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Propositions without connectives not allowed in: " + string)

    def test_invalidFormula_propositions4(self):
        string = 'p0 AND NOT p0 AND'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Propositions without connectives not allowed in: " + string)

    # negations

    def test_invalidFormula_negation1(self):
        string = 'NOT'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("No proposition for NOT in: " + string)

    def test_invalidFormula_negation2(self):
        string = 'p0 OR NOT'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("No proposition for NOT in: " + string)

    def test_invalidFormula_negation3(self):
        string = 'p0 OR (p1 AND NOT)'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Missing proposition for NOT in: " + string)

    def test_invalidFormula_negation4(self):
        string = 'p0 NOT OR p2'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Missing proposition for NOT in: " + string)

    # brackets

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

    # implications

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

    # empty formulas

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

    # lonely numbers

    def test_invalidFormula_numbers1(self):
        string = '1'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Number without a proposition is not valid.")

    def test_invalidFormula_numbers2(self):
        string = 'p0 AND 1'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Number without a proposition is not valid.")

    def test_invalidFormula_numbers3(self):
        string = 'TOP OR p1 1'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Number without a proposition is not valid.")

    def test_invalidFormula_numbers4(self):
        string = '0 p0 OR p1'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Number without a proposition is not valid.")

    def test_invalidFormula_numbers5(self):
        string = 'p1 OR (TOP OR NOT 1)'
        try: f = Formula(string)
        except FormulaInvalidError: pass
        else: self.fail("Number without a proposition is not valid.")
        
    # double negation
    
    def test_double_negations(self):
        string = u'NOT NOT p0 AND NOT p1 AND NOT p3'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'( ¬ ¬ p₀ ∧ ¬ p₁ ) ∧ ¬ p₃'))

    # some valid formulas

    def test_validFormula1(self):
        string = 'p0 IMPL p1'
        formula = Formula(string)
        self.failUnless(isinstance(formula, Formula))

    def test_validFormula2(self):
        string = '((p0))'
        formula = Formula(string)
        self.failUnless(isinstance(formula, Formula))

    def test_validFormula3(self):
        string = 'BOTTOM OR BOTTOM OR BOTTOM'
        formula = Formula(string)
        self.failUnless(isinstance(formula, Formula))

    def test_formula_name(self):
        string = 'p0'
        formula = Formula(string, 'formula1')
        self.failUnless(formula.name == 'formula1')

    # mixed formatting

    def test_mixed_formatting1(self):
        string = u'p0 ∨ p1'
        formula = Formula(string, 'formula1')
        self.failUnless(self.tools.equal(formula.formula, u'p₀ ∨ p₁'))

    def test_mixed_formatting2(self):
        string = u'p0 ∧ NOT p₂ AND ¬⊤'
        formula = Formula(string, 'formula1')
        self.failUnless(self.tools.equal(formula.formula, u'p₀ ∧ ¬ p₂ ∧ ¬ ⊤'))

    def test_mixed_formatting3(self):
        string = u'p0 OR p₃ ∨ NOT p2 OR (¬p₂ ∧ p1)'
        formula = Formula(string, 'formula1')
        self.failUnless(self.tools.equal(formula.formula, u'p₀ ∨ p₃ ∨ ¬ p₂ ∨ ( ¬ p₂ ∧ p₁ )'))


    # bracket reduction

    def test_bracket_reduction1(self):
        string = u'(p0)'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'p₀'))

    def test_bracket_reduction2(self):
        string = u'((p0))'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'p₀'))

    def test_bracket_reduction3(self):
        string = u'(((p0)))'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'p₀'))

    def test_bracket_reduction4(self):
        string = u'(p0 AND p1) OR (p2 AND p3)'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'(p₀ ∧ p₁) ∨ (p₂ ∧ p₃)'))

    def test_bracket_reduction5(self):
        string = u'((p0 AND p1) OR (p2 AND p3))'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'(p₀ ∧ p₁) ∨ (p₂ ∧ p₃)'))

    def test_bracket_reduction6(self):
        string = u'(p0 AND p1 AND p2)'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'( p₀ ∧ p₁ ) ∧ p₂'))

    def test_bracket_reduction7(self):
        string = u'p0 OR ((p1 AND p2)) OR p3'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'( p₀ ∨ ( p₁ ∧ p₂ ) ) ∨ p₃'))

    def test_bracket_reduction8(self):
        string = u'p0 AND ((p1 AND p2)) AND p3'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'( p₀ ∧ ( p₁ ∧ p₂ ) ) ∧ p₃'))

    def test_bracket_reduction9(self):
        string = u'((p0 AND p1) AND (p2 AND p3)) AND p5'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'( ( p₀ ∧ p₁ ) ∧ ( p₂ ∧ p₃ ) ) ∧ p₅'))

    ### length()

    def test_formula_length1(self):
        string = 'p0'
        formula = Formula(string)
        self.failUnless(self.tools.length(formula.formula) == 1)

    def test_formula_length2(self):
        string = 'p0 OR p1 IMPL p2 AND p3'
        formula = Formula(string)
        self.failUnless(self.tools.length(formula.formula) == 7)

    def test_formula_length3(self):
        string = 'p0 OR p1 IMPL p2 AND NOT p3'
        formula = Formula(string)
        self.failUnless(self.tools.length(formula.formula) == 8)

    def test_formula_length4(self):
        string = 'p0 OR p1 IMPL p2 AND p0'
        formula = Formula(string)
        self.failUnless(self.tools.length(formula.formula) == 7)

    def test_formula_length5(self):
        string = 'p0 OR p1 OR p2 OR p3 OR p4 OR p5'
        formula = Formula(string)
        self.failUnless(self.tools.length(formula.formula) == 11)

    def test_formula_length6(self):
        string = 'p0 OR p0 OR p0 OR p0 OR p0'
        formula = Formula(string)
        self.failUnless(self.tools.length(formula.formula) == 9)

    ### pedantic()

    def test_pedantic1(self):
        string = 'p0 OR p1 IMPL p1 AND p2'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'( p₀ ∨ p₁ ) → ( p₁ ∧ p₂ )'))

    def test_pedantic2(self):
        string = 'p0 AND p1 AND p2'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'( p₀ ∧ p₁ ) ∧ p₂'))

    def test_pedantic3(self):
        string = 'p0 AND p1 AND p2 AND p3'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'( ( p₀ ∧ p₁ ) ∧ p₂ ) ∧ p₃'))

    def test_pedantic4(self):
        string = 'p0 OR p1 OR p2 OR p3 OR p4 OR p5'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'( ( ( ( p₀ ∨ p₁ ) ∨ p₂ ) ∨ p₃ ) ∨ p₄ ) ∨ p₅'))

    def test_pedantic5(self):
        string = 'p0 OR p1 OR p2 OR p3 OR p4 OR p5 OR p6 OR p7 OR p8 OR p9 OR p10'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'( ( ( ( ( ( ( ( ( p₀ ∨ p₁ ) ∨ p₂ ) ∨ p₃ ) ∨ p₄ ) ∨ p₅ ) ∨ p₆ ) ∨ p₇ ) ∨ p₈ ) ∨ p₉ ) ∨ p₁₀'))

    def test_pedantic6(self):
        string = 'p0 OR p1 OR (p2 AND p3 IMPL p1)'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'( p₀ ∨ p₁ ) ∨ ( ( p₂ ∧ p₃ ) → p₁ )'))

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
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'( ( p₀ ∨ p₁ ) ∨ ( p₂ ∧ p₃ ) ) ∨ p₄'))

    def test_pedantic10(self):
        string = 'p0 OR NOT p1 OR NOT p2 IMPL p0 AND p1 AND p2'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'( ( p₀ ∨ ¬ p₁ ) ∨ ¬ p₂ ) → ( ( p₀ ∧ p₁ ) ∧ p₂ )'))

    def test_pedantic11(self):
        string = 'p0 OR (p1 AND p2 AND p3) IMPL (p5 AND (p6 OR p7) AND p8)'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_pedantic, u'( p₀ ∨ ( ( p₁ ∧ p₂ ) ∧ p₃ ) ) → ( ( p₅ ∧ ( p₆ ∨ p₇ ) ) ∧ p₈ )'))

    def test_pedantic12(self): # error with modified loop variables
        string = '(p0 AND p1 IMPL p1) AND (p0 AND p1 IMPL p1)'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_nnf, u'( ( ¬ p₀ ∨ ¬ p₁ ) ∨ p₁ ) ∧ ( ( ¬ p₀ ∨ ¬ p₁ ) ∨ p₁ )'))
        
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

    def test_nnf12(self):
        string = 'NOT NOT (p0 AND p1)'
        formula = Formula(string)
        self.failUnless(formula.formula_nnf == u'( p₀ ∧ p₁ )')

    def test_nnf13(self):
        string = '(p0 OR NOT p0) AND NOT (NOT p1 AND BOTTOM) AND (NOT p1 AND (p0 OR NOT p1))'
        formula = Formula(string)
        self.failUnless(formula.formula_nnf == u'( ( p₀ ∨ ¬ p₀ ) ∧ ( p₁ ∨ ⊤ ) ) ∧ ( ¬ p₁ ∧ ( p₀ ∨ ¬ p₁ ) )')
        
    def test_nnf14(self):
        string = 'NOT BOTTOM'
        formula = Formula(string)
        self.failUnless(formula.formula_nnf == u'⊤')
        
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

    ### cnf()

    def test_cnf1(self):
        string = 'p0'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_cnf, u'p₀'))

    def test_cnf2(self):
        string = 'TOP'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_cnf, u'(p₀ ∨ ¬ p₀)'))

    def test_cnf3(self):
        string = 'TOP AND p0'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_cnf, u'(p₀ ∨ ¬ p₀) ∧ p₀'))

    def test_cnf4(self):
        string = 'TOP OR BOTTOM'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_cnf, u'((p₀ ∨ ¬p₀) ∨ p₀) ∧ ((p₀ ∨ ¬p₀) ∨ ¬p₀)'))

    def test_cnf5(self):
        string = 'NOT TOP'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_cnf, u'( p₀ ∧ ¬ p₀ )'))

    def test_cnf6(self):
        string = 'p0 OR (p1 AND p2)'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_cnf, u'(p₀ ∨ p₁) ∧ (p₀ ∨ p₂)'))

    def test_cnf7(self):
        string = '(p0 AND p1) OR (p2 AND p3)'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_cnf, u'((p₀ ∨ p₂) ∧ (p₁ ∨ p₂)) ∧ ((p₀ ∨ p₃) ∧ (p₁ ∨ p₃))'))

    def test_cnf8(self):
        string = '(p0 AND p1) AND (p2 AND (p3 OR (p4 AND p5)))'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_cnf, u'(p₀ ∧ p₁) ∧ (p₂ ∧ ((p₃ ∨ p₄) ∧ (p₃ ∨ p₅)))'))

    def test_cnf9(self):
        string = '(NOT p0 AND TOP) OR (p2 AND NOT p3 AND NOT (p4 OR p5))'
        formula = Formula(string)
        self.failUnless(self.tools.equal(formula.formula_cnf, u'( ( ( ¬ p₀ ∨ p₂ ) ∧ ( ( p₀ ∨ ¬ p₀ ) ∨ p₂ ) ) ∧ ( ( ¬ p₀ ∨ ¬ p₃ ) ∧ ( ( p₀ ∨ ¬ p₀ ) ∨ ¬ p₃ ) ) ) ∧ ( ( ( ¬ p₀ ∨ ¬ p₄ ) ∧ ( ( p₀ ∨ ¬ p₀ ) ∨ ¬ p₄ ) ) ∧ ( ( ¬ p₀ ∨ ¬ p₅ ) ∧ ( ( p₀ ∨ ¬ p₀ ) ∨ ¬ p₅ ) ) )'))

    ### equals()

    def test_equals1(self):
        f1 = Formula(u'    p0  ')
        f2 = Formula(u'p0')
        self.failUnless(self.tools.equal(f1.formula_pedantic, f2.formula_pedantic))

    def test_equals2(self):
        f1 = Formula(u'( ( ((( NOT p0 )   ))))')
        f2 = Formula(u'¬p₀')
        self.failUnless(self.tools.equal(f1.formula_pedantic, f2.formula_pedantic))

    def test_equals3(self):
        f1 = Formula(u'(NOT p0 AND TOP) OR (p2 AND NOT p3 AND NOT (p4 OR p5))')
        f2 = Formula(u'(¬p₀ ∧ ⊤) ∨ (p₂ ∧ ¬p₃ ∧ ¬(p₄ ∨ p₅))')
        self.failUnless(self.tools.equal(f1.formula_cnf, f2.formula_cnf))

    def test_equals4(self):
        f1 = Formula(u'NOT p0 IMPL p1')
        f2 = Formula(u'¬ p₀ → p₁')
        self.failUnless(self.tools.equal(f1.formula_pedantic, f2.formula_pedantic))

    def test_equals5(self):
        f1 = Formula(u'NOT ((p0 AND p1) OR (p2 OR p3))')
        f2 = Formula(u'¬ ( ( p₀ ∧ p₁ ) ∨ ( p₂ ∨ p₃ ) )')
        self.failUnless(self.tools.equal(f1.formula_pedantic, f2.formula_pedantic))

    def test_equals6(self):
        f1 = Formula(u'p0 AND NOT (NOT p1 OR p2)')
        f2 = Formula(u'p₀ ∧ ( p₁ ∧ ¬ p₂ )')
        self.failUnless(self.tools.equal(f1.formula_cnf, f2.formula_cnf))

    ### split()

    def test_split1(self):
        string = u'( p₀ ∨ ¬p₁ ) ∨ p₂'
        index = 2
        formula = Formula(string)
        f = self.tools.to_list(formula.formula)
        self.failUnless(''.join(self.tools.split(f, index)[0]) == u'p₀')
        self.failUnless(''.join(self.tools.split(f, index)[1]) == u'¬p₁')

    def test_split2(self):
        string = u'( p₀ ∨ ¬p₁ ) ∨ p₂'
        index = 6
        formula = Formula(string)
        f = self.tools.to_list(formula.formula)
        self.failUnless(' '.join(self.tools.split(f, index)[0]) == u'( p₀ ∨ ¬ p₁ )')
        self.failUnless(''.join(self.tools.split(f, index)[1]) == u'p₂')

    def test_split3(self):
        string = u'(¬p₀ ∧ (p₀ ∨ ¬p₀))'
        index = 7
        formula = Formula(string)
        self.failUnless(self.tools.equal(self.tools.split(formula.formula, index)[1], u'(p₀ ∨ ¬p₀)'))

    def test_split4(self):
        string = u'p₀ ∨ ( p₂ ∧ ( p₃ ∧ ( p₄ ∧ p₅ ) ) )'
        index = 3
        formula = Formula(string)
        self.failUnless(self.tools.equal(self.tools.split(formula.formula, index)[0], u'p₀'))
        self.failUnless(self.tools.equal(self.tools.split(formula.formula, index)[1], u'( p₂ ∧ ( p₃ ∧ ( p₄ ∧ p₅ ) ) )'))


    ### clause_set()

    def test_clauses1(self):
        string = u'p0 OR NOT p1 OR (NOT p1 AND p2)'
        formula = Formula(string)
        self.failUnless(formula.clause_set()[0], [u'p₀', u'¬p₁', u'¬p₁'])
        self.failUnless(len(formula.clause_set()) == 2)

    def test_clauses2(self):
        string = u'p0 OR p1 OR NOT p2 OR (p3 AND p4 AND NOT p5)'
        formula = Formula(string)
        self.failUnless(formula.clause_set()[0], [u'p₀', u'p₁', u'¬p₂', u'p₃'])
        self.failUnless(len(formula.clause_set()) == 3)

    def test_clauses3(self):
        string = u'NOT p1 AND (p1 IMPL NOT (p1 AND NOT p2))'
        formula = Formula(string)
        self.failUnless(formula.clause_set()[0], [u'¬p₁'])
        self.failUnless(len(formula.clause_set()) == 2)

    def test_clauses4(self):
        string = u'(NOT p0 AND TOP) OR (p2 AND NOT p3 AND NOT (p4 OR p5))'
        formula = Formula(string)
        self.failUnless(formula.clause_set()[0], [u'¬p₀', u'p₂'])
        self.failUnless(len(formula.clause_set()) == 8)

    def test_clauses5(self):
        string = u'(p0 AND p1) OR (p2 AND p3)'
        formula = Formula(string)
        self.failUnless(formula.clause_set()[0], [u'p₀', u'p₂'])
        self.failUnless(len(formula.clause_set()) == 4)

    def test_clauses6(self):
        string = u'(p0 AND p1) AND (p2 AND (p3 OR (p4 AND p5)))'
        formula = Formula(string)
        self.failUnless(formula.clause_set()[0], [u'p₀'])
        self.failUnless(len(formula.clause_set()) == 5)

    def test_clauses7(self):
        string = u'p0 OR p1 OR p2 OR p3 OR p4 OR p5 OR p6 OR p7 OR p8 OR p9 OR p10'
        formula = Formula(string)
        self.failUnless(formula.clause_set()[0], [u'p₀', u'p₁', u'p₂', u'p₃', u'p₄', u'p₅', u'p₆', u'p₇', u'p₈', u'p₉', u'p₁₀'])
        self.failUnless(len(formula.clause_set()) == 1)

    def test_clauses8(self):
        string = 'p0 OR (p1 AND p2 AND p3) IMPL (p5 AND (p6 OR p7) AND p8)'
        formula = Formula(string)
        self.failUnless(formula.clause_set()[0], [u'{¬p₀, p₅}',  u'{¬p₁, ¬p₂, ¬p₃, p₅}', u'{¬p₀, p₆, p₇}', u'{¬p₁, ¬p₂, ¬p₃, p₆, p₇}', u'{¬p₀, p₈}', u'{¬p₁, ¬p₂, ¬p₃, p₈}'])
        self.failUnless(len(formula.clause_set()) == 6)

    ### evaluate()

    def test_evaluate1(self):
        string = u'TOP'
        formula = Formula(string)
        self.failUnless(self.tools.evaluate(formula.formula_nnf) == True)

    def test_evaluate2(self):
        string = u'TOP AND (BOTTOM OR BOTTOM)'
        formula = Formula(string)
        self.failUnless(self.tools.evaluate(formula.formula_nnf) == False)

    def test_evaluate3(self):
        string = u'BOTTOM OR (BOTTOM OR (TOP AND (BOTTOM OR TOP)))'
        formula = Formula(string)
        self.failUnless(self.tools.evaluate(formula.formula_nnf) == True)

    def test_evaluate4(self):
        string = u'BOTTOM OR BOTTOM OR BOTTOM'
        formula = Formula(string)
        self.failUnless(self.tools.evaluate(formula.formula_nnf) == False)

    ### resolution()

    def test_resolution1(self):
        string = u'p0'
        formula = Formula(string)
        self.failUnless([] not in self.tools.resolution(formula))

    def test_resolution2(self):
        string = u'p0 AND NOT p0'
        formula = Formula(string)
        self.failUnless([] in self.tools.resolution(formula))

    def test_resolution3(self):
        string = u'p0 AND (NOT p0 OR p1)'
        formula = Formula(string)
        self.failUnless([] not in self.tools.resolution(formula))

    def test_resolution4(self):
        string = u'(NOT p0 AND (NOT p1 OR p2)) OR (p0 AND NOT (p1 AND NOT p0))'
        formula = Formula(string)
        self.failUnless([] not in self.tools.resolution(formula))

    def test_resolution5(self):
        string = u'(NOT p0 AND p1) OR (p0 AND NOT (p1 AND NOT p0))'
        formula = Formula(string)
        self.failUnless([] not in self.tools.resolution(formula))

    ### dchains()

    def test_dchains1(self):
        formula_list = ['p0', 'TOP OR BOTTOM']
        is_axiom = self.tools.dchains(formula_list, True)
        self.failUnless(is_axiom)

    def test_dchains2(self):
        formula_list = ['p2 OR BOTTOM']
        is_axiom = self.tools.dchains(formula_list, True)
        self.failUnless(not is_axiom)

    def test_dchains3(self):
        formula_list = ['p0 AND NOT p1', 'p0 OR TOP']
        is_axiom = self.tools.dchains(formula_list, True)
        self.failUnless(is_axiom)

    def test_dchains4(self):
        formula_list = ['p0 OR p1', 'NOT p1 AND p2']
        is_axiom = self.tools.dchains(formula_list, True)
        self.failUnless(not is_axiom)

    def test_dchains5(self):
        formula_list = ['BOTTOM OR TOP', 'p2 AND p3', 'p1 AND (p2 OR p4)']
        is_axiom = self.tools.dchains(formula_list, True)
        self.failUnless(is_axiom)

    def test_dchains6(self):
        formula_list = ['BOTTOM OR TOP', 'p2 AND (NOT p2 OR p3)', 'p1 AND (p2 OR p4)']
        is_axiom = self.tools.dchains(formula_list, True)
        self.failUnless(is_axiom)

if __name__ == "__main__":
    unittest.main()
