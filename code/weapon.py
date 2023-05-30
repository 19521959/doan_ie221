import pygame

class Weapon(pygame.sprite.Sprite):
    '''
    Class này dùng để tạo ra các vũ khí và tạo các chuyển động khi dùng vũ khí đó để tấn công
    Attribute :
      - self.sprite_type(string) : loại sprite dùng trong class này là 'weapon'
      - direction(string) : phương hướng của vũ khí khi tấn công
      - full_path : đường dẫn tới file hình ảnh
      - self.image : load hình ảnh thông qua đường dẫn full_path
    input : 
        Các hướng direction
    output : 
        Tùy theo các hướng direction sẽ cho ra các kết quả tương ứng
    '''
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        self.weapon_c = 0
        direction = player.status.split('_')[0]
        #graphic
        full_path = f'./graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        
        #placement
        
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-16,0))
        else:
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-16,0))
