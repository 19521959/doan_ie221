import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    '''
    class này dùng để tạo các thực thể có trong game
    '''
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
    '''
    Attribute 
    - self.frame_index : cho frame_index mặc định bằng 0
    - self.animation_speed : độ nhanh hoạt ảnh của thực thể
    - self.direction : phương hướng
    '''
    def move(self,speed):
        '''
        Hàm tạo các bước di chuyển và hitbox của thực thể
        input : self.direction.magnitude, self.direction.x, self.direction.y
        output : self.direction , self.hitbox.x, self.hitbox.y
        '''
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x *speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y *speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        '''
        Hàm điều chỉnh va chạm collision của các thực thể trong game
            input : direction
            output : self.direction và self.hitbox
        '''
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #go right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #go left
                        self.hitbox.left = sprite.hitbox.right
            for sprite in self.visible_sprites:
                if hasattr(sprite, 'hitbox') and sprite.hitbox != self.hitbox and sprite.hitbox.colliderect(self.hitbox) and hasattr(sprite, 'health') and self.sprite_type == 'enemy' and sprite.sprite_type != 'player':
                    if self.direction.x > 0: #go right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #go left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox) :
                    if self.direction.y > 0: #go down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #go up
                        self.hitbox.top = sprite.hitbox.bottom
            for sprite in self.visible_sprites:
                if hasattr(sprite, 'hitbox') and sprite.hitbox != self.hitbox and sprite.hitbox.colliderect(self.hitbox) and hasattr(sprite, 'health') and self.sprite_type == 'enemy' and sprite.sprite_type != 'player':
                    if self.direction.y > 0: #go down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #go up
                        self.hitbox.top = sprite.hitbox.bottom
    def wave_value(self):
        '''
        Hàm dùng để tạo tương tác giữa player và thực thể khi bị đánh trúng( khi bị đánh thì thực thể sẽ thay đổi màu trong chốt lát)
            input : value 
            output : 255 hoặc 0
        '''
        value = sin(pygame.time.get_ticks())
        if value >= 0: 
            return 255
        else: 
            return 0