#主菜单
import pygame
from .. import setup_QiDong
from .. import tools
from .. import constants_ChangLiang as C
from ..components_YouXiBuJian import info_XinXi
from pygame import mixer
import time

filepath = r"./resources/music/main_theme.ogg"
mixer.init()


class MainMenu:

    def __init__(self):
        game_info = {
            'score' : 0,
            'coin' : 0,
            'player_state' : 'small'
        }
        self.start(game_info)
        self.play_music()

    def play_music(self):


        # 加载音乐
        mixer.music.load(filepath)
        mixer.music.play(start=0.0)

        # 播放时长，没有此设置，音乐不会播放，会一次性加载完
        time.sleep(0) # 360s

        # # 音乐停止播放
        # mixer.music.stop()

    # 可以被反复调用
    def start(self, game_info):
        self.game_info = game_info
        self.setup_background()
        self.setup_player()
        self.setup_cursor()
        # 游戏里的信息窗口需要从game_info获得
        self.info = info_XinXi.Info('main_menu',self.game_info)
        self.finished = False
        self.next = 'level_GuanQia'

    #设置背景
    def setup_background(self):
        # 获取图片，并进行缩放比例
        self.background = setup_QiDong.GRAPHICS['level_1']
        self.background_rect = self.background.get_rect()# 获得整个图片的矩形
        self.background = pygame.transform.scale(self.background, (int (self.background_rect.width*C.BG_MULTI),
                                                  int (self.background_rect.height*C.BG_MULTI)))
        # 游戏的滑动窗口
        self.viewport = setup_QiDong.SCREEN.get_rect()
        # 游戏标题
        self.caption = tools.get_image(setup_QiDong.GRAPHICS['title_screen'],1,60,176,88,(255,0,220),C.BG_MULTI)#标题在图片中的位置和颜色

    # 设置玩家
    def setup_player(self):
        self.player_image = tools.get_image(setup_QiDong.GRAPHICS['mario_bros'],178,32,12,16,(0,0,0),C.BG_MULTI)


    # 设置光标
    def setup_cursor(self):
        self.cursor = pygame.sprite.Sprite()
        self.cursor.image = tools.get_image(setup_QiDong.GRAPHICS['item_objects'],25,160,8,8,(0,0,0),C.BG_MULTI)
        rect = self.cursor.image.get_rect()
        rect.x,rect.y = (220,360)
        self.cursor.rect = rect
        self.cursor.state = '1p' #状态机   一个玩家


    def update_cursor(self,keys):
        if keys[pygame.K_UP]:
            self.cursor.state = '1p'
            self.cursor.rect.y = 360
        elif keys[pygame.K_DOWN]:
            self.cursor.state = '2p'
            self.cursor.rect.y = 405
        elif keys[pygame.K_RETURN]:
            self.reset_game_info()
            if self.cursor.state == '1p':
                self.finished = True
                #main_menu阶段结束
            elif self.cursor.state == '2p':
                self.finished = True



    # 帧与帧之间的更新
    def update(self,surface,keys):

        # 调用函数，选择玩家，更新光标
        self.update_cursor(keys)

        # 屏幕要存放的图片元素和他要存放的位置
        surface.blit(self.background, self.viewport)
        surface.blit(self.caption, (170,100))#标题
        surface.blit(self.player_image, (110,490))#玩家
        surface.blit(self.cursor.image, self.cursor.rect)#光标

        # 先更新，后绘图
        self.info.update()
        self.info.draw(surface)

    def reset_game_info(self):
        self.game_info = {
            'score' : 0,
            'coin' : 0,
            'player_state' : 'small'
        }