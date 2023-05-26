from settings import *
import pygame

class Timer:
    
    def __init__(self):
       
        self.accumulated_time = 0
        self.start_time = pygame.time.get_ticks()
        self.started = False
        self.running = False
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

    def pause(self):
        
        self.running = False
        self.accumulated_time += pygame.time.get_ticks() - self.start_time

    def resume(self):
        
        self.running = True
        self.start_time = pygame.time.get_ticks()

    def get(self):
        
        if self.running:
            return (self.accumulated_time +
                    (pygame.time.get_ticks() - self.start_time))
        else:
            return self.accumulated_time

    def update(self):
        
        s = int(self.get()/1000)
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)

        text_surf = self.font.render((str('{:02}:{:02}'.format(int(minutes), int(seconds)))),False,TEXT_COLOR)
        bg_rect = pygame.Rect(600, 600 , ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        text_rect = text_surf.get_rect(center = bg_rect.center)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20),3)