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
        self.MAXIMUM_NESTING_LEVEL = 10 # TODO low for debugging; set to ~20 when productive
        
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
        self.formula_nnf = self.to_nnf(self.formula_pedantic)
        self.formula_cnf = '' #self.to_cnf(self.formula_pedantic)
    
    def check(self, formula):
        substitutes = {u'0': u'\u2080', u'1': u'\u2081', u'2': u'\u2082', u'3': u'\u2083', u'4': u'\u2084',
                       u'5': u'\u2085', u'6': u'\u2086', u'7': u'\u2087', u'8': u'\u2088', u'9': u'\u2089',
                       u'AND': self.AND, u'OR': self.OR, u'NOT': self.NOT, u'IMPL': self.IMPL,
                       u'TOP': self.TOP, u'BOTTOM': self.BOTTOM}

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
                if i == len(parts) - 1:
                        raise FormulaInvalidError('illegal conjunction')
        
        # removing spaces
        formula = ''.join(f)
        self.formula = formula
        
        if self.length() == 0:
            raise FormulaInvalidError('empty formula')
        
        return f
    
    def recursive_search(self, formula, index, direction):
        print 'recursive search with', ' '.join(formula), ', idx =', index, 'dir =', direction
        if formula.count('(') > self.MAXIMUM_NESTING_LEVEL:
            raise MaximalNestingSizeError('maximal nesting size reached.')
        
        if direction == 'left':
            d = -1
        elif direction == 'right':
            d = 1
        else:
            raise ValueError
        
        pos = index + d
        
        if formula[pos].startswith('p'):
            return pos
        else:
            local_level = 0
            while True:
                #print 'checking', formula[pos], ', pos =', pos, ', local_level =', local_level
                if formula[pos] == ')':
                    local_level -= 1
                elif formula[pos] == '(':
                    local_level += 1
                
                if local_level == 0 and formula[pos][0] in ['p', '(', ')']:
                    return pos
                pos += d
    
    def to_pedantic(self, formula):
        # Description:
        # 1. AND, OR before IMPL: p0 OR p1 IMPL p2 ==> (p0 OR p1) IMPL p2
        # 2. ANDs/ORs with brackets from left to right: p0 OR p1 OR p2 OR p3 ==> (((p0 OR p1) OR p2) OR p3)
        # generate error if ANDs/ORs mixed on one level
        
        formula = self.to_list(formula)
        max_level = 0
        target_level = 0
        current_level = 0
        conj = []
        positions = []
        print "\nFormula:", ' '.join(formula)
        
        while target_level <= max_level:
            current_level = 0
            print '\nActual goal level:', target_level, ', max_level =', max_level
            for i in range(len(formula)):
                if formula[i] == ')' and current_level == target_level or i == len(formula) - 1: # and current_level == 1:
                    print "in the correct level. conj = ", conj
                    
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
                        
                        print 'pos_groups:', pos_groups
                        
                        if len(pos_groups) == 1:
                            max_brackets = 2
                        elif len(pos_groups) == 2:
                            max_brackets = 1
                        
                        for positions in pos_groups:
                            # set brackets recursively until list has only 1 conjunction left
                            while len(positions) >= max_brackets:
                                print "setting brackets for positions =", positions
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
                print "checking", formula[i], "current_level =", current_level, ' len(conj) =', len(conj)
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
        return formula.split(' ') 
        
    def length(self):
        parts = self.to_list(self.formula)
        count = []
        conn = self.connectives
        for part in parts:
            if (part not in conn and part in count) or part in self.brackets or part == '' or part == ' ':
                continue
            count.append(part)
        return len(count)
        
    def to_nnf(self, formula):
        # TODO implement
        
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
                            formula.insert(index-1, self.NOT)
                            break
                        
                else:
                    raise FormulaInvalidError('invalid implication (no implicant found)')
        
        #print ' '.join(formula)
                        
        # 2. calculate v(A), the formula with negation only before atomic propositions
        
        return ' '.join(formula)
        
    def to_cnf(self, formula):
        # TODO implement
        return formula
        
    def latex(self):
        formula = self.formula
        substitutes = {u'\u2080': u'0', u'\u2081': u'1', u'\u2082': u'2', u'\u2083': u'3', u'\u2084': u'4',
                       u'\u2085': u'5', u'\u2086': u'6', u'\u2087': u'7', u'\u2088': u'8', u'\u2089': u'9',
                       self.AND: u'\\wedge', self.OR: u'\\vee', self.NOT: u'\\neg', self.IMPL: u'\\rightarrow',
                       self.TOP: u'\\top', self.BOTTOM: u'\\bot', u'p': u'p_'}

        for a, b in substitutes.items():
            formula = formula.replace(a, b)
        
        return formula
    
    def sat(self):
        # 1. to NNF --> in initialization
        #self.to_nnf()
        
        # 2. number of prop
        parts = self.to_list(self.formula)
        #print 'Parts: ', parts
        
        propositions = []
        for part in parts:
            if part not in (self.connectives + self.brackets):
                propositions.append(part)
        
        propositions = list(set(propositions))
        propositions.sort()
        #print 'Propositions:', propositions
        
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
        #print 'Resolving', ' '.join(x for x in l)
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
