import pygame
from settings import *
from entity import Entity
from support import *
import Item

class Enemy(Entity):
    '''
    class Enemy là class tạo ra các quái vật trong game và điều chỉnh tương tác giữa player và enemy

    '''
    def __init__(self,monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp, difficulty, visible_sprites):
        '''
        Attribute:
            #general setup
        - self.sprite_type : sprite_type là 'enemy'
        - self.status : status là 'idle'
        - self.difficulty : độ khó của quái
        - self.visible_sprites : group các thực thể enemy trong trò chơi
        
            #graphics setup
        - self.import_graphics(monster_name) : đưa hình ảnh của quái vật vào game
        - self.image : tạo hình ảnh của enemy
        - self.rect : tạo rect cho enemy
        
            #movement
        - self.hitbox : hitbox cho quái
        - self.obtacle_sprites : group các vật thể có thể cản đường người chơi
        
            #enemy stats
        - self.monster_name : tên của quái vật
        - monster_info: list chứa dữ liệu của quái vật như health, exp, speed, attack_damage, ...
        
            #player interaction
        - self.can_attack : có thể tấn công
        - self.attack_time : thời gian tấn công 
        - self.attack_cooldown : khoảng thời gian chờ giữa các đòn tấn công
        - self.damage_player : sát thương có thể gây ra cho player
        - self.trigger_death_particles : kích hoạt hiệu ứng khi quái bị đánh bại
        - self.add_exp : exp của quái mà người chơi nhận được khi giết thành công
        
            #invincibility timer
        - self.vulnerable : quái có thể bị tấn công
        - self.hit_time : khoảng thời gian chờ khi bị tấn công
        - self.invincibility_duration : khoảng thời gian khi quái không thể bị nhận sát thương
        
            #sounds
        - self.death_sound : âm thanh khi quái chết
        - self.hit_sound = âm thanh khi bị đánh trúng
        - self.death_sound.set_volume : điều chỉnh đô lớn âm thanh
        - self.hit_sound.set_volume : điều chỉnh âm thanh khi bị đánh
        - self.attack_sound = âm thanh khi quái tấn công player
        - self.attack_sound.set_volume : điều chỉnh âm thanh khi tấn công
        '''
        #general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.status = 'idle'
        self.difficulty = difficulty
        self.groups_x = groups
        self.visible_sprites = visible_sprites
       
        
        #graphics setup
        self.import_graphics(monster_name)
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        
        #movement
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites
       
        #stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp'] * self.difficulty
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance'] * self.difficulty /1.5
        if difficulty > 2:
            self.health = monster_info['health'] * self.difficulty
            self.speed = monster_info['speed']* (self.difficulty / 2)
            self.attack_damage = monster_info['damage'] + (self.difficulty * 5)
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        
        #player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles =  trigger_death_particles
        self.add_exp = add_exp

        #invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 350

        #sounds
        self.death_sound = pygame.mixer.Sound('./audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('./audio/hit.wav')
        self.death_sound.set_volume(0.05)
        self.hit_sound.set_volume(0.05)
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.attack_sound.set_volume(0.04)


    def import_graphics(self, name):
        '''
        Hàm dùng để đưa hình ảnh vào game
            input : self.animation
            output : vẽ ra các hoạt ảnh từng trạng thái của quái vật như idle, move hay attack
        ''' 
        self.animations = {
            'idle':[],
            'move':[],
            'attack':[],
        }
        main_path = f'./graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        '''
        Hàm dùng để tạo sự tương tác giữa player và quái khi hai bên va chạm nhau trong khoảng cách nhất định
            input : distance
            output : distance, direction
        '''
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2() 

        return (distance, direction)

    def get_status(self, player):
        '''
        Hàm này xuất ra trạng thái của quái tùy thuộc khoảng cách của quái và player
            input : distance
            output : trạng thái của quái
        '''
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'
    
    def animate(self):
        '''
        Hàm dùng để tạo animate cho quái 
            input : self.frame_index, self.status, self.vulnerable
            output : self.can_attack, self.frame_index, self.wave_value
        '''
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        #draw the animation
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            #flicker
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        '''
        Hàm tạo cooldown cho các đòn tấn công của quái cũng như thời gian tấn công của player
            input : current_time, self.can_attack, self.attack_cooldown, self.vulnerable
            output : self.can_attack = True
                     self.vulnerable = True
        '''
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        '''
        Hàm dùng để xuất ra những sự kiện như trừ máu player, trừ máu quái vật  sau khi quái và player tấn công lẫn nhau
            input : self.vulnerable
            output : hit_sound.play()
                     health của quái sau khi bị tấn công
        '''
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()        
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
    
    def check_death(self):
        '''
        Hàm dùng để kiểm tra sự kiện chết của quái
            input : self.health 
            output : chạy kill(), trigger_death_particles, add_exp và âm thanh khi quái chết đi
        '''
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_exp(self.exp)
            self.death_sound.play()


    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def actions(self, player):
        '''
        Hàm thể hiện các hành động của quái khi đạt các điều kiện khoảng cách
            input : self.status 
            output : attack_sound.play()
                     direction
        '''
        if self.status == 'attack':
            self.attack_sound.play()
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def update(self):
        '''
        Hàm chạy các hàm hit_reaction(),move(),animate(),cooldowns(),check_deck()
        '''
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        '''
        Hàm chạy các hàm get_status(),actions()
        '''
        self.get_status(player)
        self.actions(player)
    print(__doc__)
