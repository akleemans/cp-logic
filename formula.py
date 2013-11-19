#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Represents a formula and its exceptions.

@author: adrianus
'''

import re
import locale
import time
from tools import *

locale.setlocale(locale.LC_ALL, '')

class Formula(object):
    '''
    Represents a formula.

    All symbols used are canonical and http://en.wikipedia.org/wiki/List_of_logic_symbols
    can be used as a reference.
    '''

    def __init__(self, formula, name='_anon'):
        '''
        Constructor
        '''
        # name
        self.name = name
        self.tools = Tools()

        # calculate variants and normal forms of formula
        self.formula = self.check(formula)
        self.formula_pedantic = self.to_pedantic(self.formula)
        self.formula_nnf = self.to_nnf(self.formula_pedantic)
        self.formula_cnf = self.to_cnf(self.formula_pedantic)

    def check(self, formula):
        ''' Checks if a formula is valid. '''

        substitutes = {u'0': u'\u2080', u'1': u'\u2081', u'2': u'\u2082', u'3': u'\u2083', u'4': u'\u2084',
                       u'5': u'\u2085', u'6': u'\u2086', u'7': u'\u2087', u'8': u'\u2088', u'9': u'\u2089',
                       u'AND': self.tools.AND, u'OR': self.tools.OR, u'NOT': self.tools.NOT, u'IMPL': self.tools.IMPL,
                       u'TOP': self.tools.TOP, u'BOTTOM': self.tools.BOTTOM}

        for a, b in substitutes.items():
            formula = formula.replace(a, b)

        self.validate_brackets(formula)

        # checking for illegal characters
        residue = re.sub(ur'([0-9p() \u2227\u2228\u00AC\u2192\u22A4\u22A5\u2080\u2081\u2082\u2083\u2084\u2085\u2086'
                       + ur'\u2087\u2088\u2089]+)', '', formula)
        if len(residue) != 0:
            raise FormulaInvalidError('illegal characters: '+residue)

        # removing spaces
        while len(formula) != len(formula.replace('  ', ' ')):
            formula = formula.replace('  ', ' ')

        # adding spaces
        f = ''
        for i in range(len(formula)):
            c = formula[i]
            f += c
            if c in self.tools.connectives or c in self.tools.brackets:
                if i < len(formula)-1 and formula[i+1] != ' ':
                    f += ' '
            if c in self.tools.numbers:
                if i < len(formula)-1 and formula[i+1] not in self.tools.numbers and formula[i+1] != ' ':
                    f += ' '

        # checking for propositions
        parts = f.split()
        for i in range(len(parts)):
            if parts[i] == 'p':
                raise FormulaInvalidError('propositions need an index')
            if i < len(parts)-1 and parts[i].startswith('p') and parts[i+1].startswith('p'):
                raise FormulaInvalidError('propositions need to be connected with a conjunction')

        # checking lonely numbers
        for i in range(len(formula)):
            if i == 0 and formula[i] in self.tools.numbers:
                raise FormulaInvalidError('indices must belong to a proposition')
            if formula[i] in self.tools.numbers and formula[i-1] not in self.tools.numbers + [u'p']:
                raise FormulaInvalidError('indices must belong to a proposition')

        # checking for negations
        for i in range(len(parts)):
            part = parts[i]
            if part == self.tools.NOT and i < len(parts)-1:
                if parts[i+1] == ')' or parts[i+1] in self.tools.conjunctions:
                    raise FormulaInvalidError('illegal negation')
            if part == self.tools.NOT and i == len(parts)-1:
                raise FormulaInvalidError('illegal negation')

        # checking for conjunctions
        for i in range(len(parts)):
            part = parts[i]
            if part in self.tools.conjunctions:
                if i < len(parts) - 1:
                    if parts[i+1] in self.tools.conjunctions or parts[i+1] == ')':
                        raise FormulaInvalidError('illegal conjunction')
                if i == 0:
                        raise FormulaInvalidError('illegal conjunction')
                if i == len(parts) - 1:
                        raise FormulaInvalidError('illegal conjunction')

        # removing spaces
        formula = ''.join(f)
        self.formula = formula

        # checking for empty formula
        if self.tools.length(formula) == 0:
            raise FormulaInvalidError('empty formula')

        return f

    def to_pedantic(self, formula):
        '''
        Returns the correct/pedantic form of the formula.
        The important rules here are (chapter 2.1):

            1. Negation takes precedence over AND, OR, and IMPL
                p0 AND NOT p1       ==> p0 AND (NOT p1)

            2. AND, OR take precedence over IMPL
                p0 AND p1 IMPL p2   ==> (p0 AND p1) IMPL p2

            3. AND, OR are interpreted from left to the right
                p0 AND p1 AND p2    ==> (p0 AND p1) AND p2

            4. Additionally, unnecessary brackets are removed.
                ((p0 AND p1))       ==> p0 AND p1
        '''

        formula = self.tools.to_list(formula)
        max_level = 0
        target_level = 0
        current_level = 0
        conj = []
        positions = []

        while target_level <= max_level:
            current_level = 0
            for i in range(len(formula)):
                if formula[i] == ')' and current_level == target_level or i == len(formula) - 1: # and current_level == 1:
                   # print "in the correct level. conj = ", conj

                    # check for invalid formulas.
                    a = self.tools.AND + self.tools.OR
                    b = self.tools.OR + self.tools.AND
                    conj_str = ''.join(conj)
                    if self.tools.AND in conj and self.tools.OR in conj and (a in conj_str or b in conj_str):
                        raise FormulaInvalidError('mixed AND and OR on same level')
                    elif sum([1 for x in conj if x == self.tools.IMPL]) > 1:
                        raise FormulaInvalidError('more than one implication on the same level')
                    else:
                        pos_groups = []

                        if self.tools.IMPL in conj:
                            idx = conj.index(self.tools.IMPL) #print 'Index of impl at', idx
                            pos_groups.append(positions[:idx])
                            pos_groups.append(positions[idx+1:])
                        else:
                            pos_groups.append(positions)

                        #print 'pos_groups:', pos_groups

                        if len(pos_groups) == 1:
                            max_brackets = 2
                        elif len(pos_groups) == 2:
                            max_brackets = 1

                        for positions in pos_groups:
                            # set brackets recursively until list has only 1 conjunction left
                            while len(positions) >= max_brackets:
                                #print "setting brackets for positions =", positions
                                pos = self.tools.recursive_search(formula, positions[0], 'left')
                                formula.insert(pos, '(')

                                pos = self.tools.recursive_search(formula, positions[0]+1, 'right')
                                formula.insert(pos+1, ')')

                                #conj.pop(0)
                                positions.pop(0)

                                for pos in pos_groups:
                                    for j in range(len(pos)):
                                        pos[j] += 2
                                i += 2

                    # clean up
                    conj = []
                    positions = []

                if formula[i] == ')':
                    current_level -= 1
                if formula[i] == '(':
                    current_level += 1

                max_level = max(max_level, current_level)

                # get conjunctions on current level
                if current_level == target_level:
                    if formula[i] in self.tools.conjunctions:
                        positions.append(i)
                        conj.append(formula[i])

            # finished level
            target_level += 1
            conj = []
            positions = []

        # removing brackets
        #print 'Formula before brackets:', ' '.join(formula)
        found_removable = True

        while found_removable:
            found_removable = False
            brackets = []
            current_level = 0
            for i in range(len(formula)):
                if formula[i] == '(':
                    brackets.append(str(i) + ':' + str(current_level) + str(current_level + 1))
                    current_level += 1
                if formula[i] == ')':
                    brackets.append(str(i) + ':' + str(current_level) + str(current_level - 1))
                    current_level -= 1

            #print 'formula:', ' '.join(formula)
            #print 'brackets:', brackets

            # remove multiple brackets
            for i in range(len(brackets)):
                if i < len(brackets)-1: # not operating on last element
                    if int(brackets[i].split(':')[0]) + 1 == int(brackets[i+1].split(':')[0]): # consecutive brackets
                        for j in range(i+2, len(brackets)-1): # check if ending pair matches
                            if int(brackets[j].split(':')[0]) + 1 == int(brackets[j+1].split(':')[0]) and brackets[i].split(':')[1] == brackets[j+1].split(':')[1][::-1] and brackets[i+1].split(':')[1] == brackets[j].split(':')[1][::-1]:
                                found_removable = True
                                for bracket in brackets[i+2:j]:
                                    if bracket.endswith(brackets[i+1].split(':')[1]): found_removable = False
                                if found_removable:
                                    pos1 = int(brackets[i].split(':')[0])
                                    pos2 = int(brackets[j+1].split(':')[0])
                                    #print 'Removing multiple brackets.'
                                    #print 'Before:', ' '.join(formula)
                                    formula = formula[:pos1] + formula[pos1+1:pos2] + formula[pos2+1:]
                                    #print 'After:', ' '.join(formula)
                                    break

                if found_removable: break

            # remove outer brackets
            if not found_removable and len(brackets) >= 2:
                # find outer brackets and check if they are on positions 0 and len()-1
                if brackets[0] == '0:01' and brackets[len(brackets)-1].endswith('10') and int(brackets[len(brackets)-1].split(':')[0]) == len(formula)-1:
                    found_removable = True
                    # check if they belong to the same pair
                    for bracket in brackets[1:len(brackets)-1]:
                        if bracket.endswith('10'): found_removable = False
                    if found_removable:
                        #print 'Removing outer brackets.'
                        #print 'Before:', ' '.join(formula)
                        formula = formula[1:len(formula)-1]
                        #print 'After:', ' '.join(formula)

        return ' '.join(formula)

    def sufo(self):
        ''' Returns all subformulas to a given formula. '''
        subformulas = [self.formula_pedantic]

        element_count = 0
        while element_count < len(subformulas):
            # walk through newly added elements
            for i in range(element_count, len(subformulas)):
                element = self.tools.to_list(subformulas[i])
                element_count += 1
                for j in range(len(element)):

                    # 1. conjunction rule: add both parts to the subformula set
                    if element[j] in self.tools.conjunctions:
                        idx = self.tools.recursive_search(element, j, 'left') # left part
                        new_element = ' '.join(element[idx:j])
                        if new_element not in subformulas: subformulas.append(new_element)

                        idx = self.tools.recursive_search(element, j, 'right') # right part
                        new_element = ' '.join(element[j+1:idx+1])
                        if new_element not in subformulas: subformulas.append(new_element)

                    # 2. NOT rule: add the part after the negation to the sufo-set
                    elif element[j] == self.tools.NOT:
                        idx = self.tools.recursive_search(element, j, 'right')
                        new_element = ' '.join(element[j+1:idx+1])
                        if new_element not in subformulas: subformulas.append(new_element)

        subformulas.sort(key = len)
        return subformulas

    def to_nnf(self, formula):
        '''
        Calculates the negation normal form of a given formula.
        This is done by first calculating p(A) by removing the implications
        and then calculating v(A), where negations only stand before atomic propositions.
        '''

        # 1. calculate p(A), the formula without implication
        formula = self.tools.to_list(formula)
        for i in range(len(formula)):
            if formula[i] == self.tools.IMPL: # implication found
                formula[i] = self.tools.OR
                if formula[i-1].startswith('p'):
                    formula.insert(i-1, self.tools.NOT)
                elif formula[i-1] == ')':
                    level = -1
                    for index in range(i-2, -1, -1):
                        if formula[index] == ')': level -= 1
                        elif formula[index] == '(': level += 1

                        if level == 0:
                            formula.insert(index, self.tools.NOT)
                            break

                else:
                    raise FormulaInvalidError('invalid implication (no implicant found)')

        # 2. calculate v(A), the formula with negation only before atomic propositions
        max_length = len(formula)
        i = 0
        while i < max_length:
            if formula[i] == self.tools.NOT:
                if formula[i+1] == self.tools.NOT:    # double negation found
                    formula.pop(i)
                    formula.pop(i)
                    i -= 1
                    max_length -= 2
                elif formula[i+1] == '(':      # 'bad' negation found
                    formula.pop(i)
                    formula.insert(i+1, self.tools.NOT)

                    level = 0
                    for index in range(i+2, len(formula)):
                        if formula[index] == ')': level -= 1
                        elif formula[index] == '(': level += 1

                        if level == 0 and (formula[index] in self.tools.conjunctions):
                            if formula[index] == self.tools.OR: formula[index] = self.tools.AND
                            elif formula[index] == self.tools.AND: formula[index] = self.tools.OR
                            formula.insert(index+1, self.tools.NOT)
                            break
            i += 1

        return ' '.join(formula)

    def to_cnf(self, formula):
        '''
        Calculates the conjunctive negation form of a given formula.
        As of definition 154 of the script, we apply the (sigma) and (tau)-transformation
        to obtain cnf(A) of a given formula A.

        First, TOP and BOTTOM are replaced:
        TOP ==> (p0 OR NOT p0)
        BOTTOM ==> (p0 AND NOT p0)

        Then, the following formulas are substituted:
        A OR (B1 AND B2) ==> (A OR B1) AND (A OR B2)
        (A1 AND A2) OR B ==> (A1 OR B) AND (A2 OR B)

        (A1 AND A2) OR (B1 AND B2) ==> ((A1 AND A2) OR B1) AND ((A1 AND A2) OR B2) (first step)
        '''

        # 1. replace TOP, BOTTOM
        formula = self.tools.to_list(formula)
        subst = {self.tools.TOP: u'( p\u2080 ' + self.tools.OR + ' ' + self.tools.NOT + u' p\u2080 )',
                 self.tools.BOTTOM: u'( p\u2080 ' + self.tools.AND + ' ' + self.tools.NOT + u' p\u2080 )'}

        for i in range(len(formula)):
            if formula[i] in [self.tools.TOP, self.tools.BOTTOM]:
                formula[i] = subst[formula[i]]

        # recompile formula
        temp = ' '.join(formula)
        formula = self.tools.to_list(temp)

        # 2. replace subformulas
        # get level depth
        max_level = self.tools.get_depth(formula)
        if (self.tools.VERBOSE): print 'Nesting depth:', max_level

        # replace subformulas from top level to bottom
        current_level = 0
        level = -1
        restart_level = False
        while level <= max_level: # loop over levels
            level += 1
            current_level = 0
            #print 'Checking level =', level

            for i in range(len(formula)): # loop over formula
                # if already changed formula, start again on same level
                if restart_level:
                    restart_level = False
                    level = max(level-2, -1)
                    break

                if formula[i] == '(': current_level += 1
                if formula[i] == ')': current_level -= 1

                if current_level > self.tools.MAXIMUM_NESTING_LEVEL:
                    raise MaximalNestingSizeError('maximal nesting size reached.')

                #print 'formula[i] =', formula[i], ', level =', level, ', current_level =', current_level

                if current_level == level and formula[i] == self.tools.OR: # only act if in right level. isolate A, B
                    A, B = self.tools.split(formula, i)
                    first_part = formula[0:self.tools.recursive_search(formula, i, 'left')]
                    last_part = formula[self.tools.recursive_search(formula, i, 'right')+1:len(formula)]

                    changed_part = ''
                    # check for case 1: AND in B
                    local_level = 0
                    for j in range(len(B)):
                        if B[j] == '(': local_level += 1
                        if B[j] == ')': local_level -= 1

                        # A OR (B1 AND B2) ==> (A OR B1) AND (A OR B2)
                        if local_level == 1 and B[j] == self.tools.AND:
                            B1, B2 = self.tools.split(B, j)
                            #print 'Splitting B =', ' '.join(B)
                            #print 'B1 = ', ' '.join(B1)
                            #print 'B2 = ', ' '.join(B2)
                            changed_part = ' ( ' + ' '.join(A) + ' ' + self.tools.OR + ' ' + ' '.join(B1) + ' ) '
                            changed_part += self.tools.AND + ' ( ' + ' '.join(A) + ' ' + self.tools.OR + ' ' + ' '.join(B2) + ' ) '
                            break

                    # check for case 2: AND in A
                    if changed_part == '': # only if not already case 1
                        local_level = 0
                        for j in range(len(A)):
                            if A[j] == '(': local_level += 1
                            if A[j] == ')': local_level -= 1

                            # (A1 AND A2) OR B ==> (A1 OR B) AND (A2 OR B)
                            if local_level == 1 and A[j] == self.tools.AND:
                                A1, A2 = self.tools.split(A, j)
                                #print 'Splitting A =', ' '.join(A)
                                #print 'A =', A
                                #print 'A1 = ', ' '.join(A1)
                                #print 'A2 = ', ' '.join(A2)
                                changed_part = ' ( ' + ' '.join(A1) + ' ' + self.tools.OR + ' ' + ' '.join(B) + ' ) '
                                changed_part += self.tools.AND + ' ( ' + ' '.join(A2) + ' ' + self.tools.OR + ' ' + ' '.join(B) + ' ) '
                                break

                    if changed_part != '':
                        formula = ' '.join(first_part) + changed_part + ' '.join(last_part)
                        #print 'rebuilding formula.'
                        #print 'A =', ' '.join(A)
                        #print 'B =', ' '.join(B)
                        #print 'first part: ', ' '.join(first_part)
                        #print 'changed part: ', changed_part
                        #print 'last part: ', ' '.join(last_part)
                        #print 'formula =', formula
                        formula = self.tools.to_list(formula)
                        self.validate_brackets(formula) # check
                        max_level = self.tools.get_depth(formula)
                        #print 'New nesting depth:', max_level
                        restart_level = True

        if (self.tools.VERBOSE): print 'CNF: returning formula =', ' '.join(formula)
        return ' '.join(formula)

    def validate_brackets(self, formula):
        '''
        Checks if the brackets for a formula are valid.
        This includes that every bracket must be closed and that no bracket pair can
        be closed before it has been opened (negative level depth).
        '''

        # checking for brackets
        level_depth = 0
        for c in formula:
            if c == '(':
                level_depth += 1
            elif c == ')':
                level_depth -= 1
            if level_depth < 0:
                raise FormulaInvalidError('brackets in illegal order')

        if level_depth > 0:
            raise FormulaInvalidError('too many opening brackets')
        if level_depth < 0:
            raise FormulaInvalidError('too many closing brackets')

        return

    def latex(self):
        ''' Returns the formula in LaTeX-syntax. '''
        formula = self.formula
        substitutes = {u'\u2080': u'0', u'\u2081': u'1', u'\u2082': u'2', u'\u2083': u'3', u'\u2084': u'4',
                       u'\u2085': u'5', u'\u2086': u'6', u'\u2087': u'7', u'\u2088': u'8', u'\u2089': u'9',
                       self.AND: u'\\wedge', self.OR: u'\\vee', self.NOT: u'\\neg', self.IMPL: u'\\rightarrow',
                       self.TOP: u'\\top', self.BOTTOM: u'\\bot', u'p': u'p_'}

        for a, b in substitutes.items():
            formula = formula.replace(a, b)

        return formula

### exceptions ###

class FormulaInvalidError(Exception):
    def __init__(self, arg):
        self.value = arg

class TimeOutError(Exception):
    def __init__(self, arg):
        self.value = arg

class MaximalNestingSizeError(Exception):
    def __init__(self, arg):
        self.value = arg

class UnexpectedTokenError(Exception):
    def __init__(self, arg):
        self.value = arg

