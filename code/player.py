import pygame
from settings import *
from support import import_folder
from entity import Entity
from Dashing import *

class Player(Entity):
    
    def __init__(self,pos,groups, obstacle_sprites, create_attack, destroy_attack, create_magic, visible_sprites, toggle_gachapon, timer):
        
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/images/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6 ,HITBOX_OFFSET['player'])
        self.visible_sprites = visible_sprites
        self.timer = timer

        #graphics setup
        self.import_player_assets()
        self.status = 'down'
        self.display_surface = pygame.display.get_surface()
        #task
        self.sprite_type = 'player'
        self.dead = False
        #movement

        self.attacking = False
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        #weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 400

        #magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.switch_duration_cooldown = 400

        #stats
        self.stats = {'health': 100,'energy':60,'attack': 10,'magic': 4,'speed': 5}
        self.max_stats = {'health': 1000, 'energy': 1000, 'attack': 400, 'magic' : 100, 'speed': 15}
        self.upgrade_cost = {'health': 1500, 'energy': 1500, 'attack': 800, 'magic' : 1000, 'speed':3000}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 0
        self.speed = float(self.stats['speed'])
        self.recovery_rate = 0.008 * self.stats['magic']
        self.attack_cooldown = 400


        #invincibility timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        #import sounds
        self.weapon_attack_sound = pygame.mixer.Sound('./audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.05)
        self.g_o_ft = True
        self.game_over = pygame.mixer.Sound('./audio/GameOver.wav')
        self.game_over.set_volume(1)


        self.is_player = True
        self.font = pygame.font.Font(UI_FONT, 50)
        self.restart_pressed = False

        #gacha
        self.toggle_gachapon = toggle_gachapon

    def input(self):
        
        if self.health > 0:
            keys = pygame.key.get_pressed()

            #movement input
            if keys[pygame.K_UP] and not 'attack' in self.status:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] and not 'attack' in self.status:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT] and not 'attack' in self.status:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT] and not 'attack' in self.status:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0


            #attack input
            if keys[pygame.K_z] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()
            #magic input
            if keys[pygame.K_c] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)

            #switch magic
            if keys[pygame.K_w] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < len(magic_data.keys()) -1:
                    self.magic_index += 1
                else: 
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]


            #switch wep
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(weapon_data.keys()) -1:
                    self.weapon_index += 1
                else: 
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]

    def energy_recovery(self):
       
        if self.energy <= self.stats['energy']:
            self.energy += self.recovery_rate
        else:
            self.energy = self.stats['energy']

    def write_to_file(self, data):
        
        with open('./save/save.txt','a') as score_file:
            score_file.write(data + '\n')

    def check_death(self):
        
        if self.health < 0:
            self.timer.pause()
            if self.dead == False:
                s = int(self.timer.get()/1000)

                self.write_to_file(str(s))
                self.dead = True
            title_surf = self.font.render('Press Enter to play again', False, (255,255,255))
            if self.g_o_ft:
                self.game_over.play()
                self.g_o_ft = False
            title_rect = title_surf.get_rect(center = (650, 300))
            self.display_surface.blit(title_surf, title_rect)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.restart_pressed = True

    def item_pickup(self):
        
        for sprite in self.visible_sprites:
            if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'item':
                if sprite.item_name == 'potion':
                    if sprite.hitbox.colliderect(self.hitbox):
                        sprite.pick_up_sound.play()
                        self.health = min(self.health + 20, self.stats['health'])
                        sprite.kill()
                elif sprite.item_name == 'scroll':
                    if sprite.hitbox.colliderect(self.hitbox):
                        sprite.pick_up_sound.play()
                        for enemy in self.visible_sprites:
                            if hasattr(enemy, 'sprite_type') and enemy.sprite_type == 'enemy':
                                enemy.health = 0
                                sprite.kill()
                elif sprite.item_name == 'chest':
                    if sprite.hitbox.colliderect(self.hitbox):
                        sprite.pick_up_sound.play()
                        self.toggle_gachapon()
                        sprite.kill()

    def cooldowns(self):
        
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True 

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True 

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def import_player_assets(self):
        
        character_path = './graphics/player/'
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [], 'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
            'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': [],
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_status(self):
        

        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        
        if self.attacking:
            # self.direction.x = 0
            # self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    #overwrite idle
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def animate(self):
        
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        #draw the animation
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        #flicker
        if not self.vulnerable:
            #flicker
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
       
        return list(self.upgrade_cost.values())[index]

    def get_current_values_by_index(self, index):
        
        return list(self.stats.values())[index]

    def update(self):
        
        self.input()
        self.item_pickup()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()
        self.check_death()
 

    