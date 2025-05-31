import os

import pygame

class Game:
    # 设置游戏界面，比如游戏屏幕大小
    def __init__(self,state_dict,start_state):

        # 获得屏幕、钟
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()

        self.state_dict = state_dict#状态字典
        self.state = state_dict[start_state]#初始状态赋值

    def update(self):
       if self.state.finished:#像链表一样更新状态
            game_info = self.state.game_info
            next_state = self.state.next
            self.state.finished = False
            self.state = self.state_dict[next_state]
            self.state.start(game_info)
       self.state.update(self.screen,self.keys)

    #开始游戏
    def run(self):
        # 更新->画图->更新->画图->更新……
        while True:
            # 更新部分  从pygame上不断获取鼠标键盘上的信息
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # 事件信息为退出
                    pygame.display.quit()
                elif event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()

            self.update()#更新游戏画面

            # 画图部分
            pygame.display.update()#更新画面
            self.clock.tick(60)#每秒钟5帧

# 加载所有图片文件到字典    路径，图片类型
def load_graphics(path,accept = ('.jpg','.png','.bmp','.gif')):
    graphics = {}
    # 使用os来分析path，是python的一种内置系统
    for pic in os.listdir(path):
        name , ext = os.path.splitext(pic)#拆分成文件+后缀
        # 如果是可允许格式，便载入图片
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(path,pic))
            # 如果图片是透明底，那便载入成透明底形式的图片
            if img.get_alpha():
               img = img.convert_alpha()
            else:
                img = img.convert()
            graphics[name] = img#存放入字典
    return graphics

# 从加载好的图片中获取某部分图片的方法
def get_image(sheet,x,y,width,height,colorkey,scale):
    # 用方框在素材中框取图片
    # sheet 传入图片
    # x、y为方框左上方角的坐标，width height是方框的宽高
    # colorkey是快速抠图的颜色
    # scale是放大倍数

    # image为新创建的空图层，和图片大小相同
    image = pygame.Surface((width,height))
    image.blit(sheet,(0,0),(x,y,width,height))#用bill方法给自身画出传入的图，00表示话到哪个位置，xywh表示sheet里哪个区域需要取出来
    image.set_colorkey(colorkey)#底色快速抠图
    # 放大图篇
    image = pygame.transform.scale(image,(int (width*scale),int(height*scale)))
    return image