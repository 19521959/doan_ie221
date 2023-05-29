import math
import pygame
from settings import *

class Highscore:
    '''
    Class tạo object Highscore, dùng để xếp hạng giờ chơi.

    '''
    def __init__(self):
        '''
        Hàm khởi tạo cho class Highscore.
        Attribute:
            #general setup
            self.display_surface (pygame.Surface): Surface màn hình game
            self.score_list (list): list các highscore
            self.attribute_nr (int): số lượng highscore
            self.font (pygame.font.Font): font chữ 
            self.font2 (pygame.font.Font): font chữ title 

            #item creation
            self.height (int): độ cao item
            self.width (int): độ rộng item
        '''
        #general setup
        self.display_surface = pygame.display.get_surface()
        self.score_list = self.read_score()
        self.attribute_nr = len(self.score_list)
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.font2 = pygame.font.Font(UI_FONT, 50)

        #item creation
        self.height = self.display_surface.get_size()[1] * 0.1
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

    def read_score(self):
        '''
        Hàm đọc và sắp xếp điểm từ file txt (theo thứ tự từ lớn đến bé)
        Attributes:
            x (list): list các phần tử thời gian xếp từ lớn đến bé
        return:
            5 phần tử đầu tiên của x
        '''
        with open('./save/save.txt','r') as score_file:
            x = sorted(map(lambda x: int (x) , score_file.readlines()), reverse= True)
        return x[0:5]

    def create_items(self):
        '''
        Hàm tạo các phần tử trong list item có thể roll
        Attributes:
            self.item_list (list): list các item (ui)
            full_width (int): độ dài màn hình
            increment (int): khoảng cách giữa các phần tử
            left (int): vị trí các phần tử
            item (Item): tạo object item
        output: thêm các item vào list tương ứng
        '''
        self.item_list = []

        for item, index in enumerate(range(self.attribute_nr)):
            #horizontal position
            full_height = self.display_surface.get_size()[1]
            left = self.display_surface.get_size()[0] * 0.42

            #vertical position
            top = (100 + index * 100)
            #create object
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)


    def display(self):
        '''
        Hàm thực thi các method của class Gacha, đồng thời hiển thị các phần tử
        '''
        text_surf = self.font2.render('HIGHSCORE',False,TEXT_COLOR)
        bg_rect = pygame.Rect(600, 10 , 80, 80)
        text_rect = text_surf.get_rect(center = bg_rect.center)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20),3)

        for index, item in enumerate(self.item_list):
            s = int(self.score_list[index])

            hours, remainder = divmod(s, 3600)
            minutes, seconds = divmod(remainder, 60)
            #get attributes
            name = str('{:02}:{:02}'.format(int(minutes), int(seconds)))

            item.display(self.display_surface, name)

class Item:
    '''
    Class Item chuyên dùng để tạo các phần tử cho class Highscore.

    '''
    def __init__(self, l, t, w, h, index, font):
        '''
        Hàm khởi tạo cho class Item (Highscore)
        Attributes:
            - l (int): vị trí left
            - t (int): vị trí top
            - w (int): độ rộng
            - h (int): độ cao
            - index (int): index của item
            
            - font (pygame.font): font chữ chính
            - self.rect (pygame.Rect): rect item
            - self.index (int): index item được chọn.
            - self.font (pygame.font): font chữ chính.

        '''    
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font


    def display_names(self, surface, name):
        '''
        Hàm hiển thị tên của phần tử, thay đổi màu chữ tuỳ theo trạng thái.
        input:
            - surface (pygame.Surface): Surface màn hình game
            - name (str): tên phần tử
            - selected (bool): trạng thái chọn
        Attributes:
            - color (color): màu chữ
            - name (str): tên phần tử
        '''
        color = TEXT_COLOR

        #title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))

        #draw
        surface.blit(title_surf, title_rect)


    def display(self, surface, name):
        '''
        Hàm thực thi các method của class Item.
        '''
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
        pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        self.display_names(surface, name)