#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Node for applying the deduction chain (dchain)-algorithm.

@author: adrianus
'''

import locale
import tools
import formula

locale.setlocale(locale.LC_ALL, '')

class Node(object):
    '''
    Represents a node in a dchain-tree.
    Each node has 0-2 children, depending on its chain.
    '''

    def __init__(self, chain, name, edge='', parent=None):
        ''' Constructor '''
        self.tools = tools.Tools()

        self.name = name
        self.chain = chain
        #self.chain = formula.Formula(chain).formula_nnf.replace(' ', '')
        self.parent = parent
        self.edge = edge
        self.children = []
        self.axiom = 'reducible' # undef, no, id, true
        self.status = ''

    def set_position(self, x, y):
        '''
        Sets the position of the node on the graph.
        '''
        self.x = x
        self.y = y

    def set_status(self, status):
        '''
        Sets the status (e.g. if the user clicked on it).
        '''
        self.status = status

    def traverse_tree(self):
        '''
        Traverses tree and its child nodes.
        Returns if it ends in an axiom (True) or if not (False).
        '''
        
        if self.is_axiom():
            return True
        
        self.calculate_children()
        
        if len(self.children) == 0:
            # not an axiom and no children ==> irreducible
            return False
        elif len(self.children) == 1:
            return self.children[0].traverse_tree()
        elif len(self.children) == 2:
            children_status = []
            children_status.append(self.children[0].traverse_tree())
            children_status.append(self.children[1].traverse_tree())
            return (children_status[0] and children_status[1])

    def calculate_children(self):
        '''
        Calculates the children from a given chain.
        The rules from PSC apply, an OR leads to 1 child whereas an AND leads to 2 children.
        '''
        self.children = []

        for i in range(len(self.chain.split(','))-1, -1, -1):
            part = self.chain.split(',')[i]
            #print 'searching part =', part
            part = formula.Formula(part).formula_nnf.replace(' ', '')

            current_level = 0
            min_level = 1000
            pos = 0
            for j in range(len(part)):
                if part[j] == ')': current_level -= 1
                if part[j] == '(': current_level += 1

                if part[j] in [self.tools.OR, self.tools.AND] and current_level < min_level:
                    pos = j
                    min_level = current_level

            if min_level != 1000:
                first_part = ','.join(self.chain.split(',')[:i])
                if first_part != '': first_part = first_part + ','
                last_part = ','.join(self.chain.split(',')[i+1:])
                if last_part != '': last_part = ',' + last_part

                if part[pos] == self.tools.OR:
                    self.children.append(Node(first_part + part[:pos] + ',' + part[pos+1:] + last_part, self.name + '0', self.tools.OR, self))
                    break

                elif part[pos] == self.tools.AND:
                    chain1 = first_part + part[:pos] + last_part
                    chain2 = first_part + part[pos+1:] + last_part
                    self.children.append(Node(chain1, self.name + '0', self.tools.AND, self))
                    self.children.append(Node(chain2, self.name + '1', self.tools.AND, self))
                    break

                if len(self.children) > 0:
                    break

    def is_axiom(self):
        '''
        Checks if current node is an axiom or not.
        There are two kinds of axioms in PSC:

            1. (True): a TOP is isolated
            2. (Id): an atomic proposition and also its negation are isolated
        '''

        # break up chain
        formulas = self.chain.split(',')
        for i in range(len(formulas)):
            formulas[i] = formulas[i].strip()

        # check for TOPs
        for i in range(len(formulas)):
            if formulas[i] == self.tools.TOP:
                self.axiom = 'true'
                return True

        # check for propositions
        for i in range(len(formulas)):
            for j in range(i+1, len(formulas)):
                if formulas[i] == self.tools.negated(formulas[j]):
                    self.axiom = 'id'
                    return True

        # not an axiom. check other two cases
        if len(self.children) > 0:
            self.axiom = 'reducible'
        else:
            self.axiom = 'no'
        return False
