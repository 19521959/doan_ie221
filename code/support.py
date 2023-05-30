from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    '''
    Hàm import các file csv vào list
    Attributes:
        - terrain_map (list): chứa các list chứa các ký hiệu của file csv 
    return:
        - List chứa nhiều list tạo thành ma trận 2 chiều có thông tin của bản đồ
    '''
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter= ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    '''
    Hàm import folder, đường dẫn đến folder chứa các file hình ảnh
    Attributes:
        surface_list (list): chứa đường dẫn đến tất cả các file trong folder
    return:
        list chứa đường dẫn đến các file trong folder
    '''
    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list