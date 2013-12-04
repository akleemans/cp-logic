#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Tools-class for use with formulas.

@author: adrianus
'''

import re
import locale
import time

import formula
import node
import tree

locale.setlocale(locale.LC_ALL, '')

class Tools(object):
    '''
    Static tools as an addition for the formula-class.
    All algorithms not directly associated with the formula itself are part of this class.
    Also holds the constants for nesting level and verbosity.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # static
        self.MAXIMUM_NESTING_LEVEL = 20
        self.MAXIMUM_RESOLUTION_SIZE = 50
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

        self.numbers = [u'\u2080', u'\u2081', u'\u2082', u'\u2083', u'\u2084',
                        u'\u2085', u'\u2086', u'\u2087', u'\u2088', u'\u2089']

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

    def length(self, formula):
        ''' Returns the length of a given formula. '''
        parts = self.to_list(formula)
        count = []
        for part in parts:
            if part not in self.brackets and part != '' and part != ' ':
                count.append(part)
        return len(count)

    def get_depth(self, formula):
        ''' Returns the depth (= maximal nesting level) of a formula. '''
        max_level = 0
        current_level = 0
        for part in formula:
            if part == '(': current_level += 1
            elif part == ')': current_level -= 1
            max_level = max(current_level, max_level)

        return max_level

    def sat(self, formula_nnf):
        '''
        Returns if a given formula is satisfiable by brute forcing through all possibilities.
        Will return the first valuation (if existing) which satisfies the formula.
        Expects a formula in NNF.
        '''
        parts = self.to_list(formula_nnf)

        propositions = []
        for part in parts:
            if part not in (self.connectives + self.brackets):
                propositions.append(part)

        propositions = list(set(propositions))
        propositions.sort()

        high = 2**len(propositions)
        if (self.VERBOSE): print 'Found', len(propositions), 'distinct propositions =>', high, 'possibilities'

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

    def evaluate(self, formula_nnf):
        '''
        Wrapper around resolve(), built for user input.
        Will be called from the main class.
        '''
        formula = self.to_list(formula_nnf)

         # replace TOP and BOTTOM with t and f
        for i in range(len(formula)):
            if formula[i] == self.TOP: formula[i] = 't'
            if formula[i] == self.BOTTOM: formula[i] = 'f'

        return self.resolve(formula)

    def resolve(self, l):
        '''
        Resolves a formula with no propositions to a single value (true or false).
        For internal use only, for example by sat() or evaluate().
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

    def split(self, formula, i):
        ''' Returns the two neighbours of a conjunction. '''

        if formula[i] not in self.conjunctions:
            print 'got "' + formula[i] + '" instead'
            raise UnexpectedTokenError('can only find neighbours of conjunctions.')

        idx = self.recursive_search(formula, i, 'left')
        A = formula[idx:i]

        idx = self.recursive_search(formula, i, 'right')
        B = formula[i+1:idx+1]

        return A, B

    def resolution(self, formula):
        '''
        Applies resolution to a given formula.
        '''
        K = formula.clause_set()

        length = 0

        while len(K) != length:
            length = len(K)
            if length > self.MAXIMUM_RESOLUTION_SIZE:
                break
            #print 'length K:', len(K)

            K = self.resolution_step(K)
            if [] in K: break

        return K

    def resolution_step(self, K):
        K_new = []
        for i in range(len(K)):
            for j in range(i+1, len(K)):
                for a in K[i]:
                    #print 'checking a =', a, ', K[i] = ', K[i], ', K[j] =', K[j]
                    if self.negated(a) in K[j]:
                        new_clause = []
                        new_clause.extend(K[i])
                        new_clause.extend(K[j])
                        new_clause.remove(a)
                        new_clause.remove(self.negated(a))
                        #print 'length K[i] =', len(K[i])
                        #print 'length K[j] =', len(K[j])
                        #print 'New clause:', new_clause
                        if new_clause not in K:
                            K_new.append(new_clause)
                        #try:
                        #    new_clause = K[i].remove(a) + K[j].remove(self.negated(a))
                        #    if new_clause not in K:
                        #        if new_clause == None: K_new.append([])
                        #        else:
                        #except TypeError, e:
                        #    print 'Error: tried to add', K[i], 'and', K[j]
                        #    pass

        #print 'K =', K
        #print 'K_new =', K_new
        #print 'K + K_new =', (K + K_new)

        #if not [] in K + K_new:
        #    K = list(set(K + K_new))

        return K + K_new

    def negated(self, p):
        ''' Returns the negated proposition. '''

        if p.startswith(self.NOT):
            return p.split(self.NOT)[1]
        else:
            return self.NOT + p

    def dchains(self, formula_list, testing=False):
        '''
        Applies the 'deduction chains'-algorithm to a set of formulas.
        Out of a initial sequence G, rules are applied to obtain either a
        irreducible sequence or an axiom of PSC.
        '''

        # 1. calculating initial Gamma = Gamma0
        G = ''

        for f in formula_list:
            f1 = formula.Formula(f, '_anon')
            G = G + f1.formula_nnf.replace(' ', '') + ','
        G = G[:-1]

        # 2. build up tree by apply rules
        parent = node.Node(G, '0')
        is_axiom = parent.traverse_tree()

        # 3. draw tree
        if not testing:
            t = tree.Tree(parent)

        return is_axiom

    def recursive_search(self, formula, index, direction):
        '''
        Returns the position of the last part which lies on the same level in the formula.
        The search accepts 'left' or 'right' as direction and will stop if the beginning or end is reached.
        '''

        if direction == 'left': d = -1
        elif direction == 'right': d = 1
        else: raise ValueError

        pos = index + d
        local_level = 0

        while True:
            if pos == -1: return 0
            if pos == len(formula): return pos-1

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

    def equal(self, f1, f2):
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
