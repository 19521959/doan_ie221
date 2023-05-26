import pygame, sys
from settings import *
from level import Level
from itertools import cycle
from Highscore import Highscore
BLINK_EVENT = pygame.USEREVENT + 0
class Game:
    
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Monster Slayer')

        self.level = Level()

        #sound
        self.main_sound = pygame.mixer.Sound('./audio/wilffire.ogg')
        self.main_sound.play(loops = -1)
        self.main_sound.set_volume(0.1)
        self.accept = pygame.mixer.Sound('./audio/Accept.wav')
        self.accept.set_volume(0.1)
        self.state = 'intro'
        self.started = False
        self.font = pygame.font.Font(UI_FONT, 50)
        self.screen_rect = self.screen.get_rect()
        self.restart_f = False

        #title
        title_surf = self.font.render('Press Enter to Start', True, (255,255,255))
        self.title_rect = title_surf.get_rect(center = (self.screen_rect.center[0] - 10, self.screen_rect.center[1] - 160))
        off_text_surf = pygame.Surface(self.title_rect.size, pygame.SRCALPHA, 32)
        off_text_surf = off_text_surf.convert_alpha()
        self.blink_surfaces = cycle([title_surf, off_text_surf])
        self.blink_surf = next(self.blink_surfaces)
        pygame.time.set_timer(BLINK_EVENT, 800)
        self.instruct_image = pygame.image.load('./graphics/instruction/instruction.png')
        self.instruct_image = pygame.transform.scale(self.instruct_image, (1067,250))
        self.instruct_image.set_colorkey((22,24,52))
        self.instruct_rect = self.instruct_image.get_rect(center = (self.screen_rect.center[0], self.screen_rect.center[1] + 180))

    def intro(self):
        
        if not self.started:
            self.level.visible_sprites.custom_draw(self.level.player, self.level.render_offset, self.level.player_attacked)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.accept.play()
                        self.started = True
                        self.state = 'main_game'
                        self.level.timer.started = True
                if event.type == BLINK_EVENT:
                    self.blink_surf = next(self.blink_surfaces)
            self.screen.blit(self.instruct_image, self.instruct_rect)
            self.screen.blit(self.blink_surf, self.title_rect)
            pygame.display.update()
    
    def state_manager(self):
        
        if self.state == 'intro':
            self.intro()
        if self.state == 'main_game':
            self.main_game()
        if self.state == 'restart':
            self.restart_f = True
            self.level = Level()
            self.state = 'main_game'
            self.level.timer.started = True
    
    def main_game(self):
        
        self.screen.fill(WATER_COLOR)
        self.level.run()
        pygame.display.update()
        if self.restart_f:
            self.restart_f = False
            self.accept.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.level.toggle_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.level.toggle_ranking()
        if self.level.player.health < 0 and self.level.player.restart_pressed:
            self.state = 'restart'

    def run(self):
        
        while True:
            self.state_manager()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()