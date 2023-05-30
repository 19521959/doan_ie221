from settings import *
import pygame


class Timer:
    '''
    Class Timer dùng để tạo bộ đếm thời gian cho game
    '''
    def __init__(self):
        '''
        Hàm khởi tạo cho class Timer.
        Attributes:
            - self.accumulated_time (int): Thời gian đã tích luỹ
            - self.start_time (pygame.Time): Thời gian bắt đầu
            - self.started (bool): hàm kiểm tra Timer chạy hay chưa
            - self.running (bool): hàm kiểm tra Timer có đang chạy hay không
            - self.display_surface (pygame.Surface): Surface màn hình game
            - self.font (pygame.font): font chữ
        '''
        self.accumulated_time = 0
        self.start_time = pygame.time.get_ticks()
        self.started = False
        self.running = False
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

    def get(self):
        '''
        Hàm get lấy thời gian chạy của class Timer
        return:
            Nếu đang chạy thì
                - self.accumulated_time + (pygame.time.get_ticks() - self.start_time)
            còn không phải thì
                - self.accumulated_time
            
        '''
        if self.running:
            return (self.accumulated_time +
                    (pygame.time.get_ticks() - self.start_time))
        else:
            return self.accumulated_time

    def pause(self):
        '''
        Hàm tạm dừng pause cho class Timer
        '''
        self.running = False
        self.accumulated_time += pygame.time.get_ticks() - self.start_time

    def resume(self):
        '''
        Hàm tiếp tục resume cho class Timer
        '''
        self.running = True
        self.start_time = pygame.time.get_ticks()

    def update(self):
        '''
        Hàm update hiển thị thời gian theo format định sẵn qua các tính toán
        Attributes:
            s: thời gian đã tích luỹ (giây)
        '''
        s = int(self.get()/1000)
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)

        text_surf = self.font.render(
            (str('{:02}:{:02}'.format(int(minutes), int(seconds)))), False, TEXT_COLOR)
        bg_rect = pygame.Rect(600, 600, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        text_rect = text_surf.get_rect(center=bg_rect.center)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,
                         text_rect.inflate(20, 20), 3)
