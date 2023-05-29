import math
import pygame
from settings import *
from random import randint

class Gacha:
    '''
    Class tạo object Gacha dùng để quay các vật phẩm khi nhân vật nhặt rương báu
    '''
    def __init__(self, player):
        '''
        Hàm khởi tạo cho class Gachapon.
        input:
            player (Player): người chơi
         Attributes:
            #general setup
            - self.display_surface (pygame.Surface): Surface màn hình game
            - self.player (Player): người chơi từ input level
            - self.font (pygame.font): font chữ
            - self.display_gacha (bool): Biến kiểm tra gacha có đang bật hay không
            - self.rolling (bool): Biến kiểm tra gacha có đang quay hay không
            - self.give (bool): biến kiểm tra có khả năng trao đồ hay không
            - self.done (bool): biến kiểm tra gacha đã hoàn thành hay chưa

            #item creation
            - self.height (int): độ height item
            - self.width  (int): độ width item
            - self.rollable_items (list): list các item có thể roll
            - self.attribute_nr (int): số item có thể roll
            - self.create_items(): hàm tạo item dựa trên các item có thể roll
            - self.rand_item (int): random thời gian roll item
            - self.timer (int): thời gian đệm sau khi roll xong item

            #selection system
            - self.selection_index (int): index item hiện tại
            - self.selection_time (time): thời gian select item
            - self.can_move (bool): biến kiểm tra khả năng di chuyển
            - self.move_fx (pygame.mixer.Sound): âm thanh khi di chuyển
            - self.done_fx (pygame.mixer.Sound): âm thanh khi hoàn thành gacha
        '''

        #general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        self.font = pygame.font.Font(UI_FONT, 15)
        self.display_gacha = True
        self.rolling = False
        self.give = True
        self.done = False

        #item creation
        self.height = 128
        self.width = 128
        self.rollable_items = ['beef', 'honey', 'magic_wand', 'tea_leaf']
        self.attribute_nr = len(self.rollable_items)
        self.create_items()
        self.rand_item = randint(1, 70)
        self.timer = self.rand_item + 50

        #selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.move_fx = pygame.mixer.Sound('./audio/Menu1.wav')
        self.move_fx.set_volume(0.3)
        self.done_fx = pygame.mixer.Sound('./audio/Success3.wav')
        self.done_fx.set_volume(0.3)


    def rolling_item(self):
        '''
        Hàm roll item cho Gachapon.
        input:
            - self.rand_item (int): random thời gian roll item
            - self.rolling (bool): Biến kiểm tra gacha có đang quay hay không
            - self.can_move (bool): biến kiểm tra khả năng di chuyển
            - self.selection_index (int): index item hiện tại
            - self.attribute_nr (int): số item có thể roll
        output:
            Nếu hoàn thành xong việc lấy index item roll ra thì set self.rolling = False

        '''
        if self.rand_item > 0:
            self.rolling = True
            self.rand_item -= 1
            if self.can_move:
                if self.selection_index < self.attribute_nr - 1:
                    self.selection_index += 1
                    self.move_fx.play()
                    self.can_move = False
                    self.selection_time = pygame.time.get_ticks()
                else:
                    self.selection_index = 0
                    self.move_fx.play()
                    self.can_move = False
                    self.selection_time = pygame.time.get_ticks()
        else: self.rolling = False
    
    def give_item(self):
        '''
        Hàm đưa item cho người chơi
        Attributes:
            - self.gift
        output:
            - Tạo biến gift = item được chọn
            - Tăng chỉ số thuộc tính cho người chơi dựa trên tên item
            - set self.give = False
        '''
        self.gift = self.rollable_items[self.selection_index]
        if  self.gift == 'beef':
            self.player.stats['health'] += 20
        elif self.gift == 'honey':
            self.player.stats['speed'] += 0.3
        elif self.gift == 'magic_wand':
            self.player.stats['magic'] += 5
        else:
            self.player.stats['energy'] += 10
        self.give = False



    def create_items(self):
        '''
        Hàm tạo các phần tử trong list item có thể roll
        Attributes:
            - self.item_list (list): list các item
            - full_width (int): độ rộng màn hình
            - increment (int): khoảng cách giữa các phần tử
            - left (int): vị trí các phần tử
            - item (Item): tạo object item
        output: thêm các item vào list tương ứng
        '''
        self.item_list = []

        for item, index in enumerate(range(len(self.rollable_items))):
            #horizontal position
            full_width = self.display_surface.get_size()[0]
            increment = full_width // len(self.rollable_items)
            left = (item * increment) + (increment - self.width) // 2

            #vertical position
            top = self.display_surface.get_size()[1] * 0.2

            #create object
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def selection_cooldown(self):
        '''
        Hàm cooldown khi roll các phần tử.
        '''
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 150:
                self.can_move = True

    def display(self):
        '''
        Hàm thực thi các method của class Gacha, đồng thời hiển thị các phần tử item
        '''
        self.rolling_item()
        if not self.rolling and self.give:
            self.give_item()
        self.selection_cooldown()
        self.timer -= 1
        if self.give == False and self.done == False:
            self.done_fx.play() 
            self.done = True
        if self.timer < 0: 
            self.display_gacha = False
        for index, item in enumerate(self.item_list):
            #get attributes
            name = self.rollable_items[index]
            item.display(self.display_surface, self.selection_index, name)

    def isdone(self):
        return not self.display_gacha

class Item:
    '''
    Class Item chuyên dùng để tạo các phần tử cho class Gacha.

    '''
    def __init__(self, l, t, w, h, index, font):
        '''
        Hàm khởi tạo cho class Item (Gachapon)
        input:
            - l (int): vị trí left
            - t (int): vị trí top
            - w (int): độ rộng width
            - h (int): độ cao height
            - index (int): index của item
            - font (pygame.font): font chữ 
        Attributes:
            - self.rect (pygame.Rect): rect item
            - self.index (int): index item được chọn
            - self.font (pygame.font): font chữ 

        '''
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font

    def display_names(self, surface, name, selected):
        '''
        Hàm hiển thị tên của phần tử, thay đổi màu chữ tuỳ theo trạng thái chưa roll và được roll trúng.
        input:
            - surface (pygame.Surface): Surface màn hình game
            - name (str): tên phần tử
            - selected (bool): trạng thái được chọn
        Attributes:
            - color (color): màu chữ
            - name (str): tên phần tử
        '''
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        name = name.replace('_', ' ')

        #title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))


        #draw
        surface.blit(title_surf, title_rect)

    def display_images(self, surface, name, selected):
        ''' 
        Hàm hiển thị hình ảnh của phần tử
        input:
            - surface (pygame.Surface): Surface màn hình game
            - name (str): tên phần tử
            selected (bool): trạng thái chọn
        Attributes:
            - full_path (path): đường dẫn của hình ảnh item
            - image_surf (pygame.Surface): surface của hình ảnh item
        '''
        #image
        full_path = './graphics/item/' + name +'/idle/0.png'
        image_surf = pygame.image.load(full_path).convert_alpha()
        if name == 'magic_wand':
            image_surf = pygame.transform.scale(image_surf, (15,54))
        else:
            image_surf = pygame.transform.scale(image_surf, (48,48))
        image_rect = image_surf.get_rect(center = self.rect.center)

        #draw
        surface.blit(image_surf, image_rect)
    

    def display(self, surface, selection_num, name):
        '''
        Hàm thực thi các method của class Item và hiện tên và ảnh của item
        '''
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        self.display_names(surface, name, self.index == selection_num)
        self.display_images(surface, name, self.index == selection_num)