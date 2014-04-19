#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Example for drawing dchains.

@author: adrianus
'''

import locale
import pygame
from pygame.locals import *
import time
import random
import math
import os
import sys

import tools
import formula
import node

locale.setlocale(locale.LC_ALL, '')

BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
GRAY = (192, 192, 192)
WHITE = (255,255,255)

class Tree(object):
    '''
    Represents a tree structure for deduction chains.
    '''

    def __init__(self, start_node):
        '''
        Constructor
        '''
        self.start_node = start_node
        self.size = (1200, 1000)
        self.nodes = []

        # calculate depth
        self.depth = self.get_depth()
        self.image_size = (max((2**self.depth)*50, self.size[0]), 1000)
        #print self.depth

        # assign coordinates to nodes
        self.nodes = self.get_nodes()
        self.set_coordinates()

        # preparing canvas
        pygame.init()
        pygame.display.set_caption("dchains-tree")
        self.disp = pygame.display.set_mode([self.size[0], self.size[1]], RESIZABLE)
        
        self.dispRect = self.disp.get_rect()
        self.world = pygame.Surface((self.image_size[0], self.image_size[1]))
        
        self.ratio = (1.0 * self.dispRect.width) / self.world.get_width()
        scrollThick = 20
        self.track = pygame.Rect(self.dispRect.left, self.dispRect.bottom - scrollThick, self.dispRect.width, scrollThick)   
        self.knob = pygame.Rect(self.track)
        self.knob.width = self.track.width * self.ratio
        self.scrolling = False

        while not self.catch_event():
            self.draw_board()
            time.sleep(0.1)

    def resource_path(self, relative):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)

    def set_coordinates(self):
        y_step = self.image_size[1]/(self.depth+1)
        y = 0

        # assign coordinates
        for node in self.nodes:
            depth_of_node = len(node.name)
            y = y_step * depth_of_node

            if node.parent == None:
                x = self.image_size[0]/2
            else:
                x = node.parent.x
                x_step = (self.image_size[0]/(2**(len(node.name)-1))) / 2
                if node.name[-1] == '0': x -= x_step
                elif node.name[-1]  == '1': x += x_step

            node.set_position(x, y)

    def get_nodes(self):
        '''
        Traverse tree and collect all nodes into a linear list, 'nodes'.
        '''
        nodes = []
        temp = [self.start_node]

        while len(temp) > 0:
            temp.extend(temp[0].children)
            nodes.append(temp[0])
            del temp[0]

        return nodes


    def get_depth(self):
        '''
        Get the maximum depth of the tree.
        Used to calculate how to place the nodes.
        '''
        depth = 0
        nodes = []
        nodes.append(self.start_node)

        while len(nodes) > 0:
            depth = max(depth, len(nodes[0].name))
            nodes.extend(nodes[0].children)
            del nodes[0]

        return depth

    def draw_board(self):
        '''
        Starts up a pygame-canvas and draws the graph.
        '''
        self.world.fill(WHITE)
        #pygame.draw.rect(self.world, (254, 254, 254), (0, 0, self.image_size[0], self.image_size[1]))
        
        #small_font = pygame.font.SysFont(u'dejavuserif', 14)
        #normal_font = pygame.font.SysFont(u'monospace', 16)
        
        small_font = pygame.font.Font(self.resource_path(os.path.join('data', 'lucidasansuni.ttf')), 14)
        normal_font = pygame.font.Font(self.resource_path(os.path.join('data', 'lucidasansuni.ttf')), 16)
        
        for node in self.nodes:
            # precalculate labels
            name = str(len(node.name)) + '_' + node.name[-1]
            label = small_font.render(name, 1, BLACK)
            edge_label = small_font.render(node.edge, 1, BLACK)
            x_offset = label.get_width()/2
            y_offset = label.get_height()/2

            # draw line to parent
            if node.parent != None:
                pygame.draw.line(self.world, GRAY, (node.parent.x, node.parent.y), (node.x, node.y), 1)
                # draw edge label
                self.world.blit(edge_label, ((node.parent.x + node.x)/2, (node.parent.y + node.y)/2))

            # draw label
            self.world.blit(label, (node.x-x_offset, node.y-y_offset))

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
            pygame.draw.rect(self.world, circle_color, (node.x-x_offset-5, node.y-y_offset-2, x_offset*2+10, y_offset*2+4), 2)
            #pygame.draw.circle(self.disp, circle_color, (node.x+5, node.y+7), 20, 2)

            # draw if node is currently active
            if node.status == 'marked':
                label = normal_font.render(node.chain, 1, BLACK)
                #print 'Size of label:', label.get_width()
                self.world.blit(label, (node.x-label.get_width()/2+5, node.y-40))

        self.disp.blit(self.world, ((self.knob.left / self.ratio) * -1 , 0))
        pygame.draw.rect(self.disp, WHITE, self.track, 0 )
        pygame.draw.rect(self.disp, BLUE, self.knob.inflate(0,-5), 2)
            
        pygame.display.flip()

    def catch_event(self):
        '''
        Catches events like mouse clicks or buttons.
        Currently only clicking is supported.
        '''
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_click(pygame.mouse.get_pos())
            if event.type == pygame.QUIT:
                pygame.quit()
                return True

            elif event.type == VIDEORESIZE:
                self.size = event.dict['size']
                self.disp = pygame.display.set_mode([self.size[0], self.size[1]], RESIZABLE)
                self.set_coordinates()

            elif (event.type == pygame.MOUSEMOTION and self.scrolling):
                if event.rel[0] != 0:
                    move = max(event.rel[0], self.track.left - self.knob.left)
                    move = min(move, self.track.right - self.knob.right)

                    if move != 0:
                        self.knob.move_ip((move, 0))
                            
            elif event.type == pygame.MOUSEBUTTONDOWN and self.knob.collidepoint(event.pos):
                self.scrolling = True
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                self.scrolling = False

    def handle_click(self, pos):
        '''
        Checks on which node the user clicked.
        '''
        for s in self.nodes:
            s.set_status('')
            if self.distance(pos, (s.x, s.y)) < 20:
                s.set_status('marked')

    def distance(self, pos1, pos2):
        '''
        Calculate distance between two points on the graph.
        '''
        return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
