#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Represents a formula and its exceptions.

@author: adrianus
'''

import re
import locale
import time

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

        # static
        self.MAXIMUM_NESTING_LEVEL = 20
        self.VERBOSE = False

        self.brackets = ['(', ')']

        self.NOT = u'\u00AC'
        self.AND = u'\u2227'
        self.OR = u'\u2228'
        self.IMPL = u'\u2192'
        self.conjunctions = [self.AND, self.OR, self.IMPL]

        self.TOP = u'\u22A4'
        self.BOTTOM = u'\u22A5'
        self.atomic_propositions = [self.TOP, self.BOTTOM]
        self.connectives = self.conjunctions + [self.NOT] + self.atomic_propositions

        self.numbers = [u'\u2080', u'\u2081', u'\u2082', u'\u2083', u'\u2084', u'\u2085', u'\u2086', u'\u2087',
                        u'\u2088', u'\u2089']


        # calculate variants and normal forms of formula
        self.formula = self.check(formula)
        self.formula_pedantic = self.to_pedantic(self.formula)
        if (self.VERBOSE): print 'pedantic:', self.formula_pedantic
        self.formula_nnf = self.to_nnf(self.formula_pedantic)
        self.formula_cnf = self.to_cnf(self.formula_pedantic)

    def check(self, formula):
        ''' Checks if a formula is valid. '''

        substitutes = {u'0': u'\u2080', u'1': u'\u2081', u'2': u'\u2082', u'3': u'\u2083', u'4': u'\u2084',
                       u'5': u'\u2085', u'6': u'\u2086', u'7': u'\u2087', u'8': u'\u2088', u'9': u'\u2089',
                       u'AND': self.AND, u'OR': self.OR, u'NOT': self.NOT, u'IMPL': self.IMPL,
                       u'TOP': self.TOP, u'BOTTOM': self.BOTTOM}

        for a, b in substitutes.items():
            formula = formula.replace(a, b)

        self.validate_brackets(formula)

        # checking for illegal characters
        residue = re.sub(ur'([0-9p() \u2227\u2228\u00AC\u2192\u22A4\u22A5\u2080\u2081\u2082\u2083\u2084\u2085\u2086'
                       + ur'\u2087\u2088\u2089]+)', '', formula)
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
        for i in range(len(parts)):
            if parts[i] == 'p':
                raise FormulaInvalidError('propositions need an index')
            if i < len(parts)-1 and parts[i].startswith('p') and parts[i+1].startswith('p'):
                raise FormulaInvalidError('propositions need to be connected with a conjunction')

        # checking lonely numbers
        for i in range(len(formula)):
            if i == 0 and formula[i] in self.numbers:
                raise FormulaInvalidError('indices must belong to a proposition')
            if formula[i] in self.numbers and formula[i-1] not in self.numbers + [u'p']:
                raise FormulaInvalidError('indices must belong to a proposition')

        # checking for negations
        for i in range(len(parts)):
            part = parts[i]
            if part == self.NOT and i < len(parts)-1:
                if parts[i+1] == ')' or parts[i+1] in self.conjunctions:
                    raise FormulaInvalidError('illegal negation')
            if part == self.NOT and i == len(parts)-1:
                raise FormulaInvalidError('illegal negation')

        # checking for conjunctions
        for i in range(len(parts)):
            part = parts[i]
            if part in self.conjunctions:
                if i < len(parts) - 1:
                    if parts[i+1] in self.conjunctions or parts[i+1] == ')':
                        raise FormulaInvalidError('illegal conjunction')
                if i == 0:
                        raise FormulaInvalidError('illegal conjunction')
                if i == len(parts) - 1:
                        raise FormulaInvalidError('illegal conjunction')

        # removing spaces
        formula = ''.join(f)
        self.formula = formula

        if self.length() == 0:
            raise FormulaInvalidError('empty formula')

        return f

    def recursive_search(self, formula, index, direction):
        ''' Returns the position of the part which lies on the same level in the formula. '''

        if direction == 'left':
            d = -1
        elif direction == 'right':
            d = 1
        else:
            raise ValueError

        pos = index + d

        local_level = 0
        while True:
            if formula[pos] == ')':
                local_level -= 1
            elif formula[pos] == '(':
                local_level += 1

            if local_level > self.MAXIMUM_NESTING_LEVEL:
                raise MaximalNestingSizeError('maximal nesting size reached.')

            if local_level == 0 and formula[pos][0] in ['p', '(', ')']:
                if direction == 'left' and formula[pos-1] == self.NOT:
                    return pos-1
                else:
                    return pos
            pos += d

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
        '''

        formula = self.to_list(formula)
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
                    a = self.AND + self.OR
                    b = self.OR + self.AND
                    conj_str = ''.join(conj)
                    if self.AND in conj and self.OR in conj and (a in conj_str or b in conj_str):
                        raise FormulaInvalidError('mixed AND and OR on same level')
                    elif sum([1 for x in conj if x == self.IMPL]) > 1:
                        raise FormulaInvalidError('more than one implication on the same level')
                    else:
                        pos_groups = []

                        if self.IMPL in conj:
                            idx = conj.index(self.IMPL) #print 'Index of impl at', idx
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
                                pos = self.recursive_search(formula, positions[0], 'left')
                                formula.insert(pos, '(')

                                pos = self.recursive_search(formula, positions[0]+1, 'right')
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
                    if formula[i] in self.conjunctions:
                        positions.append(i)
                        conj.append(formula[i])

            # finished level
            target_level += 1
            conj = []
            positions = []

        return ' '.join(formula)

    def to_list(self, formula):
        ''' Splits a formula to a list of symbols. '''
        formula = formula.split(' ')
        formula2 = []
        for i in range(len(formula)):
            if formula[i] in self.numbers:
                formula2[-1] = formula2[-1] + formula[i].strip()
            else:
                formula2.append(formula[i].strip())

        return formula2

    def sufo(self):
        ''' Returns all subformulas to a given formula. '''
        subformulas = [self.formula_pedantic]

        element_count = 0
        while element_count < len(subformulas):
            # walk through newly added elements
            for i in range(element_count, len(subformulas)):
                element = self.to_list(subformulas[i])
                element_count += 1
                for j in range(len(element)):

                    # 1. conjunction rule: add both parts to the subformula set
                    if element[j] in self.conjunctions:
                        idx = self.recursive_search(element, j, 'left') # left part
                        new_element = ' '.join(element[idx:j])
                        if new_element not in subformulas: subformulas.append(new_element)

                        idx = self.recursive_search(element, j, 'right') # right part
                        new_element = ' '.join(element[j+1:idx+1])
                        if new_element not in subformulas: subformulas.append(new_element)

                    # 2. NOT rule: add the part after the negation to the sufo-set
                    elif element[j] == self.NOT:
                        idx = self.recursive_search(element, j, 'right')
                        new_element = ' '.join(element[j+1:idx+1])
                        if new_element not in subformulas: subformulas.append(new_element)

        subformulas.sort(key = len)
        return subformulas

    def length(self):
        ''' Returns the length of a given formula. '''
        parts = self.to_list(self.formula)
        count = []
        conn = self.connectives
        for part in parts:
            if part not in self.brackets and part != '' and part != ' ':
                count.append(part)
        return len(count)

    def to_nnf(self, formula):
        '''
        Calculates the negation normal form of a given formula.
        This is done by first calculating p(A) by removing the implications
        and then calculating v(A), where negations only stand before atomic propositions.
        '''

        # 1. calculate p(A), the formula without implication
        formula = self.to_list(formula)
        for i in range(len(formula)):
            if formula[i] == self.IMPL: # implication found
                formula[i] = self.OR
                if formula[i-1].startswith('p'):
                    formula.insert(i-1, self.NOT)
                elif formula[i-1] == ')':
                    level = -1
                    for index in range(i-2, -1, -1):
                        if formula[index] == ')': level -= 1
                        elif formula[index] == '(': level += 1

                        if level == 0:
                            formula.insert(index, self.NOT)
                            break

                else:
                    raise FormulaInvalidError('invalid implication (no implicant found)')

        # 2. calculate v(A), the formula with negation only before atomic propositions
        max_length = len(formula)
        i = 0
        while i < max_length:
            if formula[i] == self.NOT:
                if formula[i+1] == self.NOT:    # double negation found
                    formula.pop(i)
                    formula.pop(i)
                    i -= 1
                    max_length -= 2
                elif formula[i+1] == '(':      # 'bad' negation found
                    formula.pop(i)
                    formula.insert(i+1, self.NOT)

                    level = 0
                    for index in range(i+2, len(formula)):
                        if formula[index] == ')': level -= 1
                        elif formula[index] == '(': level += 1

                        if level == 0 and (formula[index] in self.conjunctions):
                            if formula[index] == self.OR: formula[index] = self.AND
                            elif formula[index] == self.AND: formula[index] = self.OR
                            formula.insert(index+1, self.NOT)
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
        formula = self.to_list(formula)
        subst = {self.TOP: u'( p\u2080 ' + self.OR + ' ' + self.NOT + u' p\u2080 )',
                 self.BOTTOM: u'( p\u2080 ' + self.AND + ' ' + self.NOT + u' p\u2080 )'}

        for i in range(len(formula)):
            if formula[i] in [self.TOP, self.BOTTOM]:
                formula[i] = subst[formula[i]]

        # recompile formula
        temp = ' '.join(formula)
        formula = self.to_list(temp)

        # 2. replace subformulas
        # get level depth
        max_level = self.get_depth(formula)
        if (self.VERBOSE): print 'Nesting depth:', max_level

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

                if current_level > self.MAXIMUM_NESTING_LEVEL:
                    raise MaximalNestingSizeError('maximal nesting size reached.')

                #print 'formula[i] =', formula[i], ', level =', level, ', current_level =', current_level

                if current_level == level and formula[i] == self.OR: # only act if in right level. isolate A, B
                    A, B = self.split(formula, i)
                    first_part = formula[0:self.recursive_search(formula, i, 'left')]
                    last_part = formula[self.recursive_search(formula, i, 'right')+1:len(formula)]

                    changed_part = ''
                    # check for case 1: AND in B
                    local_level = 0
                    for j in range(len(B)):
                        if B[j] == '(': local_level += 1
                        if B[j] == ')': local_level -= 1

                        # A OR (B1 AND B2) ==> (A OR B1) AND (A OR B2)
                        if local_level == 1 and B[j] == self.AND:
                            B1, B2 = self.split(B, j)
                            #print 'Splitting B =', ' '.join(B)
                            #print 'B1 = ', ' '.join(B1)
                            #print 'B2 = ', ' '.join(B2)
                            changed_part = ' ( ' + ' '.join(A) + ' ' + self.OR + ' ' + ' '.join(B1) + ' ) '
                            changed_part += self.AND + ' ( ' + ' '.join(A) + ' ' + self.OR + ' ' + ' '.join(B2) + ' ) '
                            break

                    # check for case 2: AND in A
                    if changed_part == '': # only if not already case 1
                        local_level = 0
                        for j in range(len(A)):
                            if A[j] == '(': local_level += 1
                            if A[j] == ')': local_level -= 1

                            # (A1 AND A2) OR B ==> (A1 OR B) AND (A2 OR B)
                            if local_level == 1 and A[j] == self.AND:
                                A1, A2 = self.split(A, j)
                                #print 'Splitting A =', ' '.join(A)
                                #print 'A =', A
                                #print 'A1 = ', ' '.join(A1)
                                #print 'A2 = ', ' '.join(A2)
                                changed_part = ' ( ' + ' '.join(A1) + ' ' + self.OR + ' ' + ' '.join(B) + ' ) '
                                changed_part += self.AND + ' ( ' + ' '.join(A2) + ' ' + self.OR + ' ' + ' '.join(B) + ' ) '
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
                        formula = self.to_list(formula)
                        self.validate_brackets(formula) # check
                        max_level = self.get_depth(formula)
                        #print 'New nesting depth:', max_level
                        restart_level = True

        if (self.VERBOSE): print 'CNF: returning formula =', ' '.join(formula)
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

    def get_depth(self, formula):
        ''' Returns the depth (= maximal nesting level) of a formula. '''
        max_level = 0
        current_level = 0
        for part in formula:
            if part == '(': current_level += 1
            elif part == ')': current_level -= 1
            max_level = max(current_level, max_level)

        return max_level

    def split(self, formula, i):
        ''' Returns the two neighbours of a conjunction. '''
        if formula[i] not in self.conjunctions:
            print 'got "' + formula[i] + '" instead'
            raise UnexpectedTokenError('can only find neighbours of conjunctions.')

        #print 'Searching with i =', i, 'formula =', formula
        idx = self.recursive_search(formula, i, 'left')
        A = formula[idx:i]

        idx = self.recursive_search(formula, i, 'right')
        B = formula[i+1:idx+1]

        return A, B

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

    def sat(self):
        '''
        Returns if a given formula is satisfiable by brute forcing through all possibilities.
        Will return the first valuation (if existing) which satisfies the formula.
        '''

        parts = self.to_list(self.formula_nnf)

        propositions = []
        for part in parts:
            if part not in (self.connectives + self.brackets):
                propositions.append(part)

        propositions = list(set(propositions))
        propositions.sort()

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
        '''
        Resolves a formula with no propositions to a single value (true or false).
        Used by sat().
        '''

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

    def equals(self, f1, f2):
        return f1.replace(' ', '') == f2.replace(' ', '')

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

