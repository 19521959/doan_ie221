'''
File chứa các cài đặt chung của game như:
- Kích thước màn hình chơi game
- Các hitbox offset
- Thiết lập kích thước, màu sắc, font chữ của UI
- Các loại màu sắc cho menu, background, border background, text,...
- Các thông tin, thuộc tính của weapon, magic, quái thú
'''
# game setup
WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 64

HITBOX_OFFSET = {
    'player': -35,
    'object': -40,
    'grass': -10,
    'invisible': -20}


# ui
BAR_HEIGHT = 25
HEALTH_BAR_WIDTH = 300
ENERGY_BAR_WIDTH = 210
ITEM_BOX_SIZE = 80
UI_FONT = './graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': './graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': './graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': './graphics/weapons/axe/full.png'},
    'rapier': {'cooldown': 50, 'damage': 8, 'graphic': './graphics/weapons/rapier/full.png'},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': './graphics/weapons/sai/full.png'}}

# magic
magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': './graphics/particles/flame/fire.png'},
    'heal': {'strength': 20, 'cost': 10, 'graphic': './graphics/particles/heal/heal.png'}}


# enemy
monster_data = {
    'squid': {'health': 50, 'exp': 100, 'damage': 20, 'attack_type': 'slash', 'attack_sound': './audio/attack/slash.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 3600},
    'raccoon': {'health': 300, 'exp': 250, 'damage': 40, 'attack_type': 'claw',  'attack_sound': './audio/attack/claw.wav', 'speed': 4, 'resistance': 1, 'attack_radius': 120, 'notice_radius': 4000},
    'spirit': {'health': 10, 'exp': 110, 'damage': 8, 'attack_type': 'thunder', 'attack_sound': './audio/attack/fireball.wav', 'speed': 6, 'resistance': 0.1, 'attack_radius': 70, 'notice_radius': 3500},
    'bamboo': {'health': 80, 'exp': 120, 'damage': 6, 'attack_type': 'leaf_attack', 'attack_sound': './audio/attack/slash.wav', 'speed': 4, 'resistance': 1, 'attack_radius': 60, 'notice_radius': 3000}}
