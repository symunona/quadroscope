#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

class Menu:
    
    lineheight = 30
    fontsize   = 28
    fontobject = None

    def __init__(self, menudata, offset = (50,20)):
        
        self.menudata = menudata
        self.selected = 0
        self.offset   = offset
        self.fontobject = pygame.font.SysFont('Arial', self.fontsize)
        self.stack = []
        
        self.actual_root = self.menudata
        
        print 'init menu 1'
        if len(self.menudata['items']) > 8 :
            print 'ou'
             
    def item(self, surface, item, index):
                        
        color = (255,255,255)        
        if (self.selected == index): color = (255,255,0)        
        surface.blit(self.fontobject.render(item['label'], 1, color), 
                     (self.offset[0], self.offset[1] + ( index * self.lineheight )))
        
    def draw(self, surface):
        for i, v in enumerate(self.actual_root['items']):
            self.item(surface, v, i)
            

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:                        
            if event.button == 4 : self.selected -= 1
            if event.button == 5 : self.selected += 1
            if self.selected >= len(self.actual_root['items']): self.selected = 0
            if self.selected < 0: self.selected = len(self.actual_root['items'])-1
            if event.button == 2 :
                if 'submenu' in self.actual_root['items'][self.selected].keys():
                    self.stack.insert(0,{'selected_index': self.selected, 'root': self.actual_root})
                    self.actual_root = self.actual_root['items'][self.selected]['submenu']
                
            if event.button == 1:
                if len(self.stack) > 0: 
                    last = self.stack.pop()                    
                    self.actual_root = last['root']
                    self.selected = last['selected_index']
