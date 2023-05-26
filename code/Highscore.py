import math
import pygame
from settings import *

class Highscore:
    
    def __init__(self):
        
        #general setup
        self.display_surface = pygame.display.get_surface()
        self.score_list = self.read_score()
        self.attribute_nr = len(self.score_list)
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.font2 = pygame.font.Font(UI_FONT, 50)

        #item creation
        self.height = self.display_surface.get_size()[1] * 0.1
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

    def read_score(self):
        
        with open('./save/save.txt','r') as score_file:
            x = sorted(map(lambda x: int (x) , score_file.readlines()), reverse= True)
        return x[0:5]

    def create_items(self):
        
        self.item_list = []

        for item, index in enumerate(range(self.attribute_nr)):
            #horizontal position
            full_height = self.display_surface.get_size()[1]
            left = self.display_surface.get_size()[0] * 0.42

            #vertical position
            top = (100 + index * 100)
            #create object
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)


    def display(self):
        
        text_surf = self.font2.render('HIGHSCORE',False,TEXT_COLOR)
        bg_rect = pygame.Rect(600, 10 , 80, 80)
        text_rect = text_surf.get_rect(center = bg_rect.center)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20),3)

        for index, item in enumerate(self.item_list):
            s = int(self.score_list[index])

            hours, remainder = divmod(s, 3600)
            minutes, seconds = divmod(remainder, 60)
            #get attributes
            name = str('{:02}:{:02}'.format(int(minutes), int(seconds)))

            item.display(self.display_surface, name)

class Item:
    
    def __init__(self, l, t, w, h, index, font):
        
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font


    def display_names(self, surface, name):
       
        color = TEXT_COLOR

        #title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))

        #draw
        surface.blit(title_surf, title_rect)


    def display(self, surface, name):
        
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
        pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        self.display_names(surface, name)