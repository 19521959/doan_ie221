from entity import Entity
import pygame
from settings import *
from support import *

class Item(Entity):
    '''
    Class này dùng để tạo các item và âm thanh khi nhặt item 
    '''
    def __init__(self, item_name, pos, groups):
        '''
        Hàm khởi tạo cho class Item (Entity)
        Attributes:
            #general setup
            - self.sprite_type : loại sprite (item)
            - self.status : trạng thái
            - self.item_name : tên item 
            
            #graphics setup
            - self.import_graphics(item_name) : đưa hình ảnh vào
            - self.image : trạng thái của hình ảnh
            - self.image(pygame.transform.scale(self.image, (64, 64))) : chuyển hình ảnh thành kích cỡ 64x64
            - self.rect : tạo rect cho hình ảnh đó

            #movement
            - self.hitbox : hitbox của item
            - self.pick_up_sound : âm thanh khi nhặt item
            - self.pick_up_sound.set_volume(0.4) : set up độ lớn âm thanh
        '''  
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
        '''
        Hàm dùng để đưa ảnh của item vào trong game
        - self.animation : lấy trạng thái hình ảnh 'idle'
        - main_path : đường dẫn tới ảnh của item đó
        input : 
        Animation trong self.animation.keys()
        ouput : 
        Đưa hình ảnh và hoạt ảnh của item đó vào trong game
        '''
        self.animations = {
            'idle':[],
        }
        main_path = f'./graphics/item/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
