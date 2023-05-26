from entity import Entity
import pygame
from settings import *
from support import *

class Item(Entity):
    
    def __init__(self, item_name, pos, groups):

        #general setup
       
        super().__init__(groups)
        self.sprite_type = 'item'
        self.status = 'idle'
        self.item_name = item_name

        #graphics setup
        
        self.import_graphics(item_name)
        self.image = self.animations[self.status][0]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft = pos)

        #movement
       
        self.hitbox = self.rect.inflate(0, -10)
        self.pick_up_sound = pygame.mixer.Sound('./audio/Magic1.wav')
        self.pick_up_sound.set_volume(0.4)

    def import_graphics(self, name):
        
        self.animations = {
            'idle':[],
        }
        main_path = f'./graphics/item/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
