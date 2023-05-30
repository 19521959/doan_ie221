import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    '''
    Class Tile dùng để tạo tile cho game và điều chỉnh sự tương tác giữa player với tile
    '''
    def __init__(self,pos,groups,sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        '''
        Hàm khởi tạo init
        Atribute:  
            - self.sprite_type : loại sprite
            - y_offset : offset của sprite_type
        input : 
            - sprite_type
        output : 
            - self.rect 
            - self.hitbox
        '''
        super().__init__(groups)

        self.sprite_type = sprite_type
        y_offset = HITBOX_OFFSET[sprite_type]
        self.image = surface
        if sprite_type == 'object':
            #do offset for object
            self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)

        if sprite_type == 'object':
            self.hitbox = self.rect.inflate(0,-64)
        else:
            self.hitbox = self.rect.inflate(0,y_offset)