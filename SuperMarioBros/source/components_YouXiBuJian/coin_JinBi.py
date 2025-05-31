import pygame
from .. import tools, setup_QiDong
from .. import constants_ChangLiang as C


class FlashingCoin(pygame.sprite.Sprite):
    def __init__(self, x=280, y=58):  # 添加x,y参数以便灵活设置位置
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        self.frame_index = 0
        frame_rects = [(1, 160, 5, 8), (9, 160, 5, 8), (17, 160, 5, 8), (9, 160, 5, 8)]
        self.load_frames(frame_rects)

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer = 0
        self.collected = False  # 标记金币是否被收集

    def load_frames(self, frame_rects):
        sheet = setup_QiDong.GRAPHICS['item_objects']
        for frame_rect in frame_rects:
            self.frames.append(tools.get_image(sheet, *frame_rect, (0, 0, 0), C.BG_MULTI))

    def update(self):
        if not self.collected:  # 只有未被收集的金币才闪烁
            current_time = pygame.time.get_ticks()
            frame_durations = [375, 125, 125, 125]

            if self.timer == 0:
                self.timer = current_time
            elif current_time - self.timer > frame_durations[self.frame_index]:
                self.frame_index += 1
                self.frame_index %= 4
                self.timer = current_time

            self.image = self.frames[self.frame_index]

    def collect(self):
        """被收集时调用"""
        self.collected = True
        self.kill()  # 从精灵组中移除