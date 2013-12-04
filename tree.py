#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Example for drawing dchains.

@author: adrianus
'''

import locale
import pygame
import time
import random
import math

import tools
import formula
import node

locale.setlocale(locale.LC_ALL, '')

BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
GRAY = (192, 192, 192)

class Tree(object):
    '''
    Represents a Tree structure .
    '''

    def __init__(self, start_node):
        self.start_node = start_node
        self.size = (1600, 900)
        self.nodes = []

        # calculate depth
        self.depth = self.get_depth()

        # assign coordinates to nodes
        y_step = self.size[1]/(self.depth+1)
        y = 0

        self.nodes = self.get_nodes()

        # assign coordinates
        for node in self.nodes:
            depth_of_node = len(node.name)
            y = y_step * depth_of_node

            if node.parent == None:
                x = self.size[0]/2
            else:
                x = node.parent.x
                x_step = (self.size[0]/(2**(len(node.name)-1))) / 2
                if node.name[-1] == '0': x -= x_step
                elif node.name[-1]  == '1': x += x_step
                #local_depth = 0
                #for token in node.name:
                #   x_step = self.size[0]/(2**local_depth+1)
                #   if token == '0': x -= x_step
                #   elif token == '1': x += x_step
                #   local_depth += 1
            node.set_position(x, y)

        #for i in range(depth):
        #    y += y_step
        #    x_step =  self.size[0]/(2**i+1)
        #    x = 0
        #    for j in range(2**i):
        #        x += x_step
                #self.shapes.append(shape.Shape(x, y, u'Γ', str(x)+'/'+str(y)))

        #values = ['undef', 'no', 'id', 'true']
        #for s in self.shapes:
        #    s.is_axiom = values[random.randint(0, 3)]

        # preparing canvas

        pygame.init()
        self.disp = pygame.display.set_mode([self.size[0], self.size[1]])
        pygame.display.set_caption("dchains-tree")

        while not self.catch_event():
            self.draw_board()
            time.sleep(0.1)

    def get_nodes(self):
        nodes = []
        temp = [self.start_node]

        while len(temp) > 0:
            temp.extend(temp[0].children)
            nodes.append(temp[0])
            del temp[0]

        return nodes


    def get_depth(self):
        depth = 0
        nodes = []
        nodes.append(self.start_node)

        while len(nodes) > 0:
            depth = max(depth, len(nodes[0].name))
            nodes.extend(nodes[0].children)
            del nodes[0]

        #print 'Found maximum depth:', depth
        return depth

    def draw_board(self):
        pygame.draw.rect(self.disp, (254, 254, 254), (0, 0, self.size[0], self.size[1]))
        small_font = pygame.font.SysFont(u'dejavuserif', 14)
        normal_font = pygame.font.SysFont(u'monospace', 16)

        for node in self.nodes:
            # precalculate label
            name = str(len(node.name)) + '_' + node.name[-1]
            label = small_font.render(name, 1, BLACK)
            x_offset = label.get_width()/2
            y_offset = label.get_height()/2

            # draw line to parent
            if node.parent != None:
                pygame.draw.line(self.disp, GRAY, (node.parent.x, node.parent.y), (node.x, node.y), 1)

            # draw label
            self.disp.blit(label, (node.x-x_offset, node.y-y_offset))

            # draw if it's an axiom or not
            circle_color = BLACK
            if node.axiom == 'true':
                circle_color = GREEN
            elif node.axiom == 'id':
                circle_color = BLUE
            elif node.axiom == 'no':
                circle_color = RED
            elif node.axiom == 'undef':
                circle_color = BLACK

            # draw node shape
            pygame.draw.rect(self.disp, circle_color, (node.x-x_offset-5, node.y-y_offset-2, x_offset*2+10, y_offset*2+4), 2)
            #pygame.draw.circle(self.disp, circle_color, (node.x+5, node.y+7), 20, 2)

            # draw if node is currently active
            if node.status == 'marked':
                label = normal_font.render(node.chain, 1, BLACK)
                #print 'Size of label:', label.get_width()
                self.disp.blit(label, (node.x-label.get_width()/2+5, node.y-40))

        pygame.display.flip()

    def catch_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_click(pygame.mouse.get_pos())
            if event.type == pygame.QUIT:
                pygame.quit()
                return True

    def handle_click(self, pos):
        for s in self.nodes:
            s.set_status('')
            if self.distance(pos, (s.x, s.y)) < 20:
                s.set_status('marked')

    def distance(self, pos1, pos2):
        return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
