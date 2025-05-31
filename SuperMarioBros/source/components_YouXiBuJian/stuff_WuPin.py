# 碰撞检测的物品

import pygame
class Item(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h,name):
        pygame.sprite.Sprite.__init__(self)
        # 虽然物品已经在背景里，但是还需添加一个图层，是他们各自拥有一个宽和高，方便检测
        self.image = pygame.Surface((w,h)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name


