
import pygame
from settings import *
from random import randint

class MagicPlayer:
    '''
    Class này dùng để tạo phần sử dụng phép thuật cho player 
    '''
    def __init__(self, animation_player):
        '''
        Hàm khởi tạo init
        Attribute:
        - self.animation_player : hoạt ảnh của player
        - self.sound : âm thanh khi dùng phép thuật để tấn công hoặc hồi máu
        - self.sounds['heal'].set_volume(0.05) : điều chỉnh âm thanh 
        - self.sounds['flame'].set_volume(0.05) : điều chỉnh âm thanh
        '''
        self.animation_player = animation_player
        self.sounds ={
            'heal': pygame.mixer.Sound('./audio/heal.wav'),
            'flame': pygame.mixer.Sound('./audio/flame.wav')
        }
        self.sounds['heal'].set_volume(0.05)
        self.sounds['flame'].set_volume(0.05)
    
    def heal(self, player, strength, cost, groups):
        '''
        Hàm tạo phương thức heal cho player 
            input : player.energy
            output : player.health tăng lên và self.sound['heal'].play()
        '''
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('heal', player.rect.center + pygame.math.Vector2(0, -30), groups)
            self.animation_player.create_particles('aura', player.rect.center, groups)

    def flame(self, player, cost, groups):
        '''
        Hàm tạo phương thức flame cho player
            input : player.energy
            output : direction lúc sử dụng phép tấn công ở hướng nào và
                     tạo các particles của phép flame trên màn hình
                     self.sound['flame'].play()
        '''
        if player.energy >= cost:
            player.energy -= cost
            self.sounds['flame'].play()
            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1,0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0,-1)
            else:
                direction = pygame.math.Vector2(0,1)
            
            for i in range(1, 6):
                if direction.x: #horizontal
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint( -TILESIZE// 3, TILESIZE // 3)
                    y = player.rect.centery + randint( -TILESIZE// 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x,y), groups)
                else: #vertical
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint( -TILESIZE// 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint( -TILESIZE// 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x,y), groups)