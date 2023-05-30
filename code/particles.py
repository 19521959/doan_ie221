import pygame
from support import import_folder
from random import choice


class AnimationPlayer:
    '''
    Class dùng để tạo các particles cho hoạt ảnh của player

    '''

    def __init__(self):
        '''
        Hàm khởi tạo init
        Attribute 
        self.frame : frame của các loại hoạt ảnh magic, attacks, monster deaths, leafs.

        '''
        self.frames = {
            # magic
            'flame': import_folder('./graphics/particles/flame/frames'),
            'aura': import_folder('./graphics/particles/aura'),
            'heal': import_folder('./graphics/particles/heal/frames'),

            # attacks
            'claw': import_folder('./graphics/particles/claw'),
            'slash': import_folder('./graphics/particles/slash'),
            'sparkle': import_folder('./graphics/particles/sparkle'),
            'leaf_attack': import_folder('./graphics/particles/leaf_attack'),
            'thunder': import_folder('./graphics/particles/thunder'),

            # monster deaths
            'squid': import_folder('./graphics/particles/smoke_orange'),
            'raccoon': import_folder('./graphics/particles/raccoon'),
            'spirit': import_folder('./graphics/particles/nova'),
            'bamboo': import_folder('./graphics/particles/bamboo'),

            # leafs
            'leaf': (
                import_folder('./graphics/particles/leaf1'),
                import_folder('./graphics/particles/leaf2'),
                import_folder('./graphics/particles/leaf3'),
                import_folder('./graphics/particles/leaf4'),
                import_folder('./graphics/particles/leaf5'),
                import_folder('./graphics/particles/leaf6'),
                self.reflect_images(import_folder(
                    './graphics/particles/leaf1')),
                self.reflect_images(import_folder(
                    './graphics/particles/leaf2')),
                self.reflect_images(import_folder(
                    './graphics/particles/leaf3')),
                self.reflect_images(import_folder(
                    './graphics/particles/leaf4')),
                self.reflect_images(import_folder(
                    './graphics/particles/leaf5')),
                self.reflect_images(import_folder(
                    './graphics/particles/leaf6'))
            )
        }

    def reflect_images(self, frames):
        '''
        Hàm tạo các ảnh lặp lại
            input : frames
            output : new_frames
        '''
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        '''
        Hàm tạo hoạt ảnh của grass
            input : animation_frames 
            output : ParticleEffect
        '''
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        '''
        Hàm tạo hoạt ảnh của các frames
            input : animation_frames
            output : ParticleEffect
        '''
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    '''
    Class dùng để tạo các hiệu ứng đặt biệt
    '''

    def __init__(self, pos, animation_frames, groups):
        '''
        Hàm khởi tạo init
        Attribute 
        - self.frame_index : cho frame index bằng 0
        - self.animation_speed : tốc độ của hoạt ảnh
        - self.frames : các hoạt ảnh frames
        - self.image : hình ảnh của frames
        - self.rect : tạo rect cho self.image
        '''
        self.sprite_type = 'magic'
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        '''
        Hàm tạo các hoạt ảnh
            input : self.frame_index
            output : self.kill() hoặc self.image
        '''
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        '''
        Chạy hàm animate()
        '''
        self.animate()
