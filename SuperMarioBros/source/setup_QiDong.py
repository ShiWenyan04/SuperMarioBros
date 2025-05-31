# 存放  游戏启动时 的代码
import pygame
from. import constants_ChangLiang as C
from. import tools
# 初始化屏幕
pygame.init()
SCREEN = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))#这里的宽高用常量表示
GRAPHICS = tools.load_graphics('resources/graphics')