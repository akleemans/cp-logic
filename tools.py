#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Tools-class for use with formulas.

@author: adrianus
'''

import re
import locale
import time

locale.setlocale(locale.LC_ALL, '')

class Tools(object):
    '''
    Some static tools as an addition for the formula-class.
    '''

    def __init__(self):
        '''
        Constructor
        '''

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

