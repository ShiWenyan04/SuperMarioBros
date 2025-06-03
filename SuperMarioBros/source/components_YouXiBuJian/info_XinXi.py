import pygame

from  ..  import constants_ChangLiang as C
from . import coin_JinBi

pygame.font.init()

#文字信息
class Info:
    # 区分各个状态要展示的不同的文字信息
    def __init__(self,state,game_info):
        self.game_info = game_info
        self.state = state
        self.create_state_labels()#用来创建某个阶段特有文字
        self.create_info_labels()#用来创建通用文字，例如时间、分数
    #    以上两中方法都会调用同一个方法  create_label 来创建文字

        self.flash_coin = coin_JinBi.FlashingCoin()#页面中闪烁的金币

    def create_state_labels(self):
        self.state_labels = []
        # 当此时状态为主菜单时
        if self.state == 'main_menu':
            self.state_labels .append((self.create_label('1 PLAYER GAME'),(272,360)))#存放文字图片和位置
            self.state_labels .append((self.create_label('2 PLAYER GAME'),(272,405)))
            self.state_labels.append((self.create_label('TOP -'),(290,465)))
            self.state_labels.append((self.create_label('000000'),(400,465)))


    def create_info_labels(self):
        self.info_labels = []
        self.info_labels.append((self.create_label('MARIO'),(75,30)))
        self.info_labels.append((self.create_label('WORD'),(450,30)))
        self.info_labels.append((self.create_label('TIME'),(625,30)))
        self.info_labels.append((self.create_label('000000'),(75,55)))
        self.info_labels.append((self.create_label('X00'),(300,55)))
        self.info_labels.append((self.create_label('1 - 1'),(480,55)))


    # 给出文字，渲染成图片返回，规定文字图片的大小
    def create_label(self,label,size=40,width_scale=1.25,height_scale=1):
        font = pygame.font.SysFont(C.FONT, size)
        #     1表示是否抗锯齿，（255，255，255）表示白色
        label_image = font.render(label, 1,(255,255,255))
        rect = label_image.get_rect()#获得图片矩形
        label_image = pygame.transform.scale(label_image,(int(rect.width*width_scale),#缩放
                                                          int (rect.height*height_scale)))
        return label_image


    # 及时更新时间分数等信息
    def update(self):
        self.flash_coin.update()

    # 显示文字、金币
    def draw(self,surface):
        # 遍历，label[0]代表图片  label[1]代表位置
        for label in self.state_labels:
            surface.blit(label[0],label[1])
        for info_label in self.info_labels:
            surface.blit(info_label[0],info_label[1])
        surface.blit(self.flash_coin.image,self.flash_coin.rect)