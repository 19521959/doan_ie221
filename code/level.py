import pygame
from Highscore import Highscore
from Timer import Timer
from magic import MagicPlayer
from particles import AnimationPlayer
from settings import *
from tile import Tile
from player import Player
from support import *
import random as rand
from random import choice, randint, random
from weapon import Weapon
from ui import UI
from enemy import Enemy
from upgrade import Upgrade
from Item import *
from gacha import Gacha

class Level:
    
    def __init__(self):
        
        #get display surface
        self.game_paused = False
        self.ui = UI()
        self.display_surface = pygame.display.get_surface()
        self.timer = Timer()

        #sprite group
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        #sprite setup
        self.layouts = {
            'boundary': import_csv_layout('./map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('./map/map_Grass_2.csv'),
            'object': import_csv_layout('./map/map_Objects_2.csv'),
            'entities': import_csv_layout('./map/map_Entities.csv')
        }

        self.graphics = {
            'grass': import_folder('./graphics/Grass'),
            'objects': import_folder('./graphics/objects'),
        }
        self.create_map()

        #particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        #upgrade
        self.upgrade = Upgrade(self.player)


        #monster spawn
        self.difficulty = 1 
        self.monster_spawn_radius = 500
        self.monster_spawn_cd = 1600
        self.monster_spawn_time = 0

        self.screen_shake = 0
        self.render_offset = [0, 0]

        self.player_attacked = 0
        self.hit_sound = pygame.mixer.Sound('./audio/Hit4.wav')
        self.hit_sound.set_volume(0.2)
        self.paused_upgrade = False
        self.paused_gacha = False
        self.paused_ranking = False
        self.game_start = False
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.highscore = Highscore()
        self.spawn_timer = 1000

    def create_magic(self, style, strength, cost):
        
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])
    
    def destroy_attack(self):
        
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None
    
    def damage_player(self, amount, attack_type):
        
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            #spawn particles
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])
            self.screen_shake = 30
            self.screen_shake_int = 14
            self.screen_shake_div= 8
            self.player_attacked = 10
            self.hit_sound.play()
           
    def trigger_death_particles(self, pos, particle_type):
        
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])
        chance = rand.random()
        if chance < 0.2:
            Item('potion', pos , [self.visible_sprites])
        if chance < 0.2:
           choice([lambda: Item('scroll', pos, [self.visible_sprites]), lambda: Item('chest', pos, [self.visible_sprites])])()



    def player_attack_logic(self):
        
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,50)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset, self.visible_sprites)
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def spawn_monster(self):
        
        current_time = pygame.time.get_ticks()
        if current_time - self.monster_spawn_time >= self.monster_spawn_cd:
    
            x = randint(8,80) * TILESIZE
            y = randint(8,52) * TILESIZE

            enemy_vec = pygame.math.Vector2(x,y)
            player_vec = pygame.math.Vector2(self.player.rect.center)
            distance = (player_vec - enemy_vec).magnitude()
            if distance >= 2000:

                monsters = randint(389,392)
                if monsters == 390: monster_name = 'bamboo'
                elif monsters == 391: monster_name = 'spirit'
                # elif monsters == 392: monster_name = 'raccoon'
                else: monster_name = 'squid'
                if monster_name == 'raccoon':
                    x = randint(7,23) * TILESIZE
                    y = randint(7,12) * TILESIZE
                self.monster_spawn_time = pygame.time.get_ticks()
                Enemy(
                    monster_name, 
                    (x,y), 
                    [self.visible_sprites, self.attackable_sprites],
                    self.obstacle_sprites,
                    self.damage_player,
                    self.trigger_death_particles,
                    self.add_exp,
                    self.difficulty,
                    self.visible_sprites
                )

    def spawnrate(self):
        
        self.spawn_timer -= 1
        if self.spawn_timer < 0:
            self.monster_spawn_cd = 1600 - (100* self.difficulty)
            self.spawn_timer = 1000

    def increase_difficulty(self, time):
        
        self.difficulty = float(time / 60)
        if self.difficulty < 1:
            self.difficulty = 1
        

    def create_attack(self):
        
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_map(self):
        
        for style, layout in self.layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col !='-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites], 'invisible')
                        
                        if style == 'grass':
                            random_grass_image = choice(self.graphics['grass'])
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites], 'grass', random_grass_image)
                        if style == 'object':
                            suf = self.graphics['objects'][int(14)]
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites], 'object', suf)
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x,y),
                                    [self.visible_sprites], 
                                    self.obstacle_sprites,
                                    self.create_attack, 
                                    self.destroy_attack,
                                    self.create_magic,
                                    self.visible_sprites,
                                    self.toggle_gacha,
                                    self.timer
                                    )
                            

    def check_screen_shake(self):
        
        if self.screen_shake > 0:
            self.screen_shake -= 1

        if self.screen_shake:
            self.render_offset[0] = randint(0, self.screen_shake_int) - self.screen_shake_div
            self.render_offset[1] = randint(0, self.screen_shake_int) - self.screen_shake_div
            
        if self.screen_shake == 0:
            self.render_offset[0] = 0
            self.render_offset[1] = 0
        if self.player_attacked > 0:
            self.player_attacked -= 1


    def run(self):
        
        self.visible_sprites.custom_draw(self.player, self.render_offset, self.player_attacked)
        if self.timer.started == True:
            self.ui.display(self.player, self.difficulty)
        if self.game_paused and self.paused_upgrade:
            self.upgrade.display()
            if self.timer.running == True:
                self.timer.pause()
        elif self.game_paused and self.paused_ranking:
            self.highscore.display()
            if self.timer.running == True:
                self.timer.pause()
        else:
            if self.paused_gacha:
                if not self.gacha.isdone():
                    self.gacha.display()
                else:
                    self.paused_gacha = not self.paused_gacha
                if self.timer.running == True:
                    self.timer.pause()
            #update and draw
            if not self.timer.running:
                self.timer.resume()
            if self.timer.started == False:
                self.timer.pause()
            if self.timer.started == True:
                self.timer.update()
            self.check_screen_shake()
            self.player_attack_logic()
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.spawn_monster()
            self.increase_difficulty(self.timer.get()/1000)
            self.spawnrate()

            
    def add_exp(self, amount):
        
        self.player.exp += amount
    
    def toggle_menu(self):
        
        self.game_paused = not self.game_paused
        self.paused_upgrade = not self.paused_upgrade
    
    def toggle_ranking(self):
       
        self.game_paused = not self.game_paused
        self.paused_ranking = not self.paused_ranking

    def toggle_gacha(self):
       
        self.gacha = Gacha(self.player)
        self.paused_gacha = True

class YSortCameraGroup(pygame.sprite.Group):
    
    def __init__(self):
        
        #setup
        super().__init__()
        #get display surface
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #floor creation
        self.floor_sur = pygame.image.load('./graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_sur.get_rect(topleft = (0,0))
        self.s = pygame.Surface((64,64), pygame.SRCALPHA)
        self.s.set_alpha(128)


    def custom_draw(self, player, render_offset, player_attacked):
        
        #get offset from player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_sur, floor_offset_pos + render_offset)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            if hasattr(sprite, 'health'):
                # pygame.draw.circle(self.display_surface, UI_BORDER_COLOR, offset_postion + [32,57], 20)
                

                mask = pygame.mask.from_surface(sprite.image).outline()
                mask = [(x, y) for x,y in mask]
                self.s.fill((0,0,0,0))
                pygame.draw.polygon(self.s, pygame.Color(0,0,0), mask)
                if sprite.sprite_type == 'enemy':
                    enemy_vec = pygame.math.Vector2(sprite.hitbox.x, sprite.hitbox.y)
                    player_vec = pygame.math.Vector2(player.rect.center)
                    distance = (player_vec - enemy_vec).magnitude()
                    if distance <= 800:
                        self.display_surface.blit(pygame.transform.flip(self.s, False, True), (offset_position[0] + render_offset[0], offset_position[1] + 64 + render_offset[0]))
                else:
                    self.display_surface.blit(pygame.transform.flip(self.s, False, True), (offset_position[0] + render_offset[0], offset_position[1] + 64 + render_offset[0]))

            if hasattr(sprite, 'weapon_c') and player.status != 'up_attack' and player.status != 'down_attack':

                mask = pygame.mask.from_surface(sprite.image).outline()
                mask = [(x, y) for x,y in mask]
                self.s.fill((0,0,0,0))
                pygame.draw.polygon(self.s, pygame.Color(0,0,0), mask)
                self.display_surface.blit(pygame.transform.flip(self.s, False, True), (offset_position[0] + render_offset[0] , offset_position[1] - 8 + render_offset[1]))
            
            if sprite.sprite_type == 'enemy':
                if distance <= 800:
                    self.display_surface.blit(sprite.image, offset_position + render_offset)
            else:
                self.display_surface.blit(sprite.image, offset_position + render_offset)


    def enemy_update(self, player):
        
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for sprite in enemy_sprites:
            sprite.enemy_update(player)