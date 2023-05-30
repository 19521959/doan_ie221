import pygame
from settings import *

class UI:
    '''
    Class dùng để tạo object UI và xử lý các tương tác của giao diện UI với game.
    '''
    def __init__(self):
        '''
        Hàm khởi tạo cho object UI
        Attributes:
            - self.display_surface (pygame.Surface): Surface màn hình game
            - self.font (pygame.font): font chữ chính của UI
            
            #bar setup
            - self.health_bar_rect (pygame.Rect): các thông số như độ cao, độ rộng, vị trí cho health bar
            - self.energy_bar_rect (pygame.Rect): các thông số như độ cao, độ rộng, vị trí cho energy bar

            #convert weapon dictionary
            - self.weapon_graphics (list): list chứa graphics của vũ khí
            
            #convert magic dictionary
            - self.magic_graphics (list): list chứa graphics của các phép
        '''
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        #bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)

        #convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
        
        #convert magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)
        

    def show_bar(self, current, max_amount, bg_rect, color):
        '''
        Hàm vẽ energy và health bar lên màn hình.
        Đồng thời cập nhật thanh energy và health bar
        input:
            - current (int): số lượng hiện tại
            - max_amount (int): số lượng max
            - bg_rect (pygame.Rect): rect background cho các thanh
            - color (color): màu của thanh trạng thái
        '''
        #drawbg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        #converting stats to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        #draw bar
        pygame.draw.rect(self.display_surface,color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,bg_rect, 3)
        pygame.draw.rect(self.display_surface, 'grey',bg_rect, 1)

    def show_exp(self,exp):
        '''
        Hàm thể hiện số lượng exp người chơi mà hiện tại đang có
        input:
            exp (int): Exp của người chơi
        '''
        text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20 
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))


        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20),3)

    def show_difficulty(self, difficulty):
        '''
        Hàm hiển thị độ khó hiện tại của level
        input:
            difficulty (float): độ khó của màn
        '''
        text_surf = self.font.render('Difficulty: '+ str('{:.2f}'.format(difficulty)),False,TEXT_COLOR)
        bg_rect = pygame.Rect(600, 10 , ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        text_rect = text_surf.get_rect(center = bg_rect.center)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20),3)

    def weapon_overlay(self, weapon_index, has_switched):
        '''
        Hàm hiển thị khung chứa vũ khí
        input:
            - weapon_index (int): index vũ khí hiện tại
            - has_switched (bool): kiểm tra khả năng switch vũ khí hiện tại
        output:
            - blit khung hình và vũ khí hiện tại lên màn hình
        '''
        bg_rect = self.selection_box(10,625, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        '''
        Hàm hiển thị khung magic
        input:
            - maigc_index (int): index magic hiện tại
            - has_switched (bool): kiểm tra khả năng switch magic hiện tại
        output:
            - blit khung hình và magic hiện tại lên màn hình
        '''
        bg_rect = self.selection_box(80,630, has_switched) #magic
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)
    
    def selection_box(self,left,top, has_switched):
        '''
        Hàm vẽ khung lựa chọn khi thay đổi vũ khí/magic
        input:
            - left (int): toạ độ left
            - top (int): toạ độ top
            - has_switched (bool): kiểm tra khả năng switch vũ khí/magic hiện tại
        output:
            - Vẽ khung UI_BORDER_COLOR_ACTIVE cho khung đang được switch
            - Hiển thị UI_BORDER_COLOR cho khung đã switch xong
        '''
        bg_rect = pygame.Rect(left, top , ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def display(self, player, difficulty):
        '''
        Hàm chạy các method của class UI
        '''
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_difficulty(difficulty)
        self.show_exp(player.exp)
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)