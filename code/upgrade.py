import math
import pygame
from settings import *

class Upgrade:
    '''
    Class dùng để thiết lập cơ chế nâng cấp cho trò chơi khi đủ lượng Exp yêu cầu

    '''
    def __init__(self, player):
        '''
        Hàm khởi tạo init
        Attribute: 
          #general setup        
          - self.display_surface : Surface màn hình
          - self.player : người chơi
          - self.attribute_nr : là độ lớn các thuộc tính của người chơi
          - self.attribute_names : là tên các thuộc tính 
          - self.font : font các thuộc tính
          - self.max_value : là chỉ số thuộc tính tối đa
          - self.current_values : là chỉ số thuộc tính hiện tại mà người chơi đang có
          
          #item creation
          - self.height : là chiều cao của item
          - self.width : là độ rộng của item
          - self.create_item() : tạo item
          
          #selection system
          - self.selection_time : là thời gian chọn nâng cấp
          - self.can_move : di chuyển khi lựa chọn nâng cấp các thuộc tính nhân vật
          - self.move_fx : bỏ âm thanh vào menu
          - self.move_fx.set_volume(0.3) : set độ lớn âm thanh của menu
        '''
        #general setup        
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.max_values = list(player.max_stats.values())
        self.current_values = list(player.stats.values())
        
        #item creation
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

        #selection system       
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.move_fx = pygame.mixer.Sound('./audio/Menu1.wav')
        self.move_fx.set_volume(0.3)

    def input(self):

        '''
        Hàm dùng để nhập các phương thức để lựa chọn các thuộc tính cần nâng cấp
          input : 
                keys[pygame.K_RIGHT],keys[pygame.K_LEFT],keys[pygame.K_UP]
          output : 
                phím Left, Right để chọn các thanh nâng cấp thuộc tính của nhân vật
                phím Up để nâng cấp stat nếu đủ điểm
        '''
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.move_fx.play()
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys [pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.move_fx.play()
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_UP]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)


    def create_items(self):

        '''
        Hàm dùng để tạo các item chứa thuộc tính
        Attribute 
          self.item_list : là danh sách các item
          #horizontal position và #vertical position : 
              Tạo tương tác giữa item và player( khoảng cách giữa các iteam, vị trí, kich thước)
          #create object : 
              Để tạo item và đưa item vào trong game 
        '''
        self.item_list = []

        for item, index in enumerate(range(self.attribute_nr)):
            #horizontal position
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (item * increment) + (increment - self.width) // 2

            #vertical position
            top = self.display_surface.get_size()[1] * 0.1

            #create object
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def selection_cooldown(self):
        '''
        Hàm dùng để set up thời gian chọn 
          input : 
                self.can_move
          output : 
                nếu self.can_move not True thì current_time(pygame.time.get_ticks)
                và nếu current_time - self.selection_time >= 150 thì self.can_move thành True
        '''
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 150:
                self.can_move = True

    def display(self):
        '''
        Hàm hiện thông tin các item thông qua hai hàm input() và selection_cooldown
          input : 
              index, item 
          output : 
              name, value, max_value, current_value, cost từng thuộc tính có thể nâng cấp
        '''
        self.input()
        self.selection_cooldown()
        
        for index, item in enumerate(self.item_list):
            #get attributes
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            current_values = self.player.get_current_values_by_index(index)
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost, current_values)

class Item:
    '''
    Class dùng để tạo các item và thanh bar
    '''
    def __init__(self, l, t, w, h, index, font):
        '''
        Hàm khởi tạo init
        Attribute
          - self.rect : tạo rect item theo left, top, width, height
          - self.index : tạo index từng item
          - self.font : tạo font chữ
          - self.up : âm thanh của item
          - self.up.set_volume : điều chỉnh độ lớn âm thanh
          - self.c_up : âm thanh menu màn hình Upgrade
          - self.c_up.set_volume : điều chỉnh độ lớn âm thanh
        '''
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font
        self.up = pygame.mixer.Sound('./audio/Gold1.wav')
        self.up.set_volume(0.3)
        self.c_up = pygame.mixer.Sound('./audio/Menu12.wav')
        self.c_up.set_volume(0.3)


    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR


        #title
        '''
          title_surf : tạo title trên surface
          title_rect : tạo rect cho title_surf
        '''
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))
        #cost
        '''
          cost_surf : tạo cost lên surface
          cost_rect : tạo rect cho cost_surf
        '''
        cost_surf = self.font.render(f'{int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(midbottom= self.rect.midbottom - pygame.math.Vector2(0,20))


        #draw
        '''
          surface.blit(title_surf, title_rect) : vẽ title lên màn hình game
          surface.blit(cost_surf, cost_rect) : vẽ cost lên màn hình game
        '''
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected, current_values):
        '''
        Hàm này dùng để vẽ thanh bar lên màn hình Upgrade. Thanh bar sẽ thay đổi màu và màu chữ trong lúc đang chọn 
        Attribute
        
          #drawing setup 
          - top với bottom : xác định vị trí bằng pygame.math.Vector2
          - color : - input : selected(thuộc tính đang chọn)
                    - output : BAR_COLOR_SELECTED hoặc BAR_COLOR
          - text_color :  - input : selected(thuộc tính đang chọn)
                          - output : TEXT_COLOR_SELECTED hoặc TEXT_COLOR
                       
          #bar setup         
          - full_height : set up chiều cao của thanh bar
          - relative_number : các số liên quan tới bar
          - value_rect : tạo rect cho value
          
          #current values
          - curr_surf : tạo current value trên surf
          - curr_rect : tạo rect cho curr_surf
          
          #draw elements 
          - pygame.draw.line() và pygame.draw.rect : vẽ surface
          - surface.blit(curr_surf, curr_rect) : vẽ current value lên màn hình
        '''
        #drawing setup 
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR
        text_color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        
        #bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value/max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        #current values
        curr_surf = self.font.render(f'{math.ceil(current_values)}', False, color)
        curr_rect = curr_surf.get_rect(midright = value_rect.midleft - pygame.math.Vector2(10,0))

        #draw elements      
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)
        surface.blit(curr_surf, curr_rect)
    
    def trigger(self, player): 
        '''
        Hàm dùng để tạo sự tương tác giữa player và thanh bar thuộc tính theo giá trị exp của nhân vật
          input : 
              - player.exp 
              - player.upgrade_cost 
              - upgrade_attribute
              - player.max_stat
          output : 
              - player.stats[upgrade_attribute]
              - player.upgrade_cost[upgrade_attribute]
          Nếu điểm thuộc tính đã nâng cấp vượt qua giá trị tối đa mà thuộc tính có thể có thì 
          set điểm thuộc tính đó bằng giá trị tối đa của thuộc tính đó.
        '''
        upgrade_attribute = list(player.stats.keys())[self.index]

        if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            self.up.play()
            player.exp -= player.upgrade_cost[upgrade_attribute]
            if upgrade_attribute != 'speed':
                player.stats[upgrade_attribute] *= 1.2
                player.upgrade_cost[upgrade_attribute] *= 1.4
            
            if upgrade_attribute == 'speed':
                player.attack_cooldown /= player.stats['speed']
                player.stats[upgrade_attribute] *= 1.2
                player.upgrade_cost[upgrade_attribute] *= 8
                pass
        else:
            self.c_up.play()

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self, surface, selection_num, name, value, max_value, cost, current_values):
        '''
        Hàm dùng để vẽ ra màn hình các thuộc tính của upgrade như name, cost, max_value, current_value
          input : 
                - self.index
          output : 
                - Bắt đầu vẽ ra hình ảnh các thuộc tính của upgrade vào màn hình game
        '''
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        self.display_names(surface, name, cost, self.index == selection_num)
        self.display_bar(surface, value, max_value, self.index == selection_num, current_values)