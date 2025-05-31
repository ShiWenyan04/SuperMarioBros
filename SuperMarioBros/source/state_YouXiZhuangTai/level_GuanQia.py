from ..components_YouXiBuJian import info_XinXi, player_ZhuJue, brick_ZhuanKuai, coin_manager
import pygame
from .. import setup_QiDong
from..import constants_ChangLiang as C
import json,os
from ..components_YouXiBuJian import stuff_WuPin,brick_ZhuanKuai,box_HeZi

class Level:
    def start(self,game_info):
        self.game_info = game_info
        # 当前阶段是否结束
        self.finished = False
        self.next =None# 下一阶段
        self.info = info_XinXi.Info('level',self.game_info)
        #    地图
        self.load_map_data()
        self.setup_start_positions()
        #   背景
        self.setup_background()
         #    马里奥
        self.setup_player()
    #     检测物品的实例
        self.setup_ground_items()
    #     砖块\宝箱
        self.setup_bricks_boxes()
    #     金币
        self.setup_coins()



    def load_map_data(self):
        file_name  = 'level_1.json'
        file_path = os.path.join('source/data/maps',file_name)
        with open(file_path) as f:
            self.map_data = json.load(f)


    # 加载背景
    def setup_background(self):
        self.image_name = self.map_data['image_name']
        self.background = setup_QiDong.GRAPHICS[self.image_name]
        # 从图片中截取得一个矩形
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width*C.BG_MULTI),
                                                                   int(rect.height*C.BG_MULTI)))

        self.background_rect = self.background.get_rect()
        # 游戏窗口大小与屏幕一致
        self.game_window = setup_QiDong.SCREEN.get_rect()
        self.game_ground = pygame.Surface((self.background_rect.width, self.background_rect.height))


    def setup_start_positions(self):
        self.positions = []
        for data in self.map_data['maps']:
            self.positions.append((data['start_x'], data['end_x'],data['player_x'], data['player_y']))
        self.start_x,self.end_x,self.player_x,self.player_y = self.positions[0]


    # 创建 马里奥对象   马里奥位置
    def setup_player(self):
        self.player = player_ZhuJue.Player('mario')
        self.player.rect.x = self.game_window.x+self.player_x
        self.player.rect.bottom = self.player_y

    def setup_ground_items(self):
        # 可以存放多个精灵、地面、楼梯、水管
        self.ground_items_group = pygame.sprite.Group()
        for name in ['ground','pipe','step']:
            for item in self.map_data[name]:
                self.ground_items_group.add(stuff_WuPin.Item(item['x'], item['y'], item['width'], item['height'], name))

    # 砖块精灵
    def setup_bricks_boxes(self):
        self.brick_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()
        if 'brick' in self.map_data:
            for box_data in self.map_data['brick']:
                x,y = box_data['x'],box_data['y']
                brick_type = box_data['type']
                if 'brick_num' in box_data:
                    pass
                else:
                    self.brick_group.add(brick_ZhuanKuai.Brick(x,y,brick_type))
        if 'box' in self.map_data:
            for box_data in self.map_data['box']:
                x,y = box_data['x'],box_data['y']
                brick_type = box_data['type']
                self.brick_group.add(box_HeZi.Box(x,y,brick_type))


    def update(self,surface, keys):
        # 更新角色位置
        self.player.update( keys)
        self.update_player_position()
        self.update_game_window(keys)  #滑动窗口
        # 页面画图
        self.draw(surface )
        self.info.update()#金币闪烁
        self.brick_group.update()
        self.box_group.update()

    # 角色位置
    def update_player_position(self):
        # x 方向
        self.player.rect.x+=self.player.x_vel
        if self.player.rect.x < self.start_x:
            self.player.rect.x = self.start_x
        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x
        self.check_x()


        #     y方向
        self.player.rect.y += self.player.y_vel
        self.check_y()

    # x方向碰撞检测   可能与马里奥碰撞的物品一一罗列，然后进行碰撞检测
    def check_x(self):
        # 该方法可检测一颗精灵是否与一个精灵族的精灵是否有碰撞
        # 会返回第一个与精灵碰撞的精灵，如果什么都没有就返回null
        # 将两个精灵组合并成一个精灵组
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group,self.box_group)
        collided_sprite = pygame.sprite.spritecollideany(self.player, check_group)
        if collided_sprite:
            self.adjust_player_x(collided_sprite)


    #         y方向碰撞检测
    def check_y(self):
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group,self.box_group)
        collided_sprite = pygame.sprite.spritecollideany(self.player, check_group)
        if collided_sprite:
            self.adjust_player_y(collided_sprite)
    #     精灵是否下落
        self.player.rect.y += 1
        check_group = pygame.sprite.Group(self.ground_items_group)
        collided = pygame.sprite.spritecollideany(self.player, check_group)
        if not collided and self.player.state == 'walk':
            self.player.state = 'fall'
        self.player.rect.y -= 1

    # 碰撞检测之后 主角的x做调整
    def adjust_player_x(self,sprite):
        if self.player.rect.x < sprite.rect.x:
            self.player.rect_right = sprite.rect.left
        elif self.player.rect.x > sprite.rect.right:
            self.player.rect_left = sprite.rect.right
        self.player.x_vel = 0
    #     碰撞检测之后，主角的y做调整
    def adjust_player_y(self,sprite):
        # 撞到地面的楼梯，管子
        if self.player.rect.bottom < sprite.rect.bottom:
            self.player.y_vel = 0
            self.player.rect.bottom = sprite.rect.top
            self.player.state = 'walk'
        else:
            # 撞到空中的箱子
            self.player.rect.top = sprite.rect.bottom
            self.player.y_vel = 7
            self.player.state = 'fall'

    # 滑动窗口
    def update_game_window(self,keys):
        # 窗口的三分之一位置
        third = self.game_window.x  + self.game_window.width
        if self.player.x_vel > 0 and self.player.rect.centerx < third and self.game_window.right < self.end_x:
            if keys[pygame.K_LEFT]:
                self.game_window.x -= self.player.x_vel
            elif keys[pygame.K_RIGHT]:
                self.game_window .x += self.player.x_vel
            self.start_x = self.game_window.x


    def setup_coins(self):
        """设置关卡中的金币"""
        self.coin_manager = coin_manager.CoinManager()
        # 可以从地图数据中读取金币位置
        if 'coins' in self.map_data:
            positions = [(coin['x'], coin['y']) for coin in self.map_data['coins']]
            self.coin_manager.setup_coins(positions)
        else:
            self.coin_manager.setup_coins()

    def check_coin_collision(self):
        if self.coin_manager.check_collision(self.player):
            self.game_info['coin'] += 1
            self.player.collect_coin()  # 播放音效
            self.info.update_coin_count()

    # 页面画图
    def draw(self, surface):


        self.game_ground.blit(self.background, self.game_window,self.game_window)
        self.game_ground.blit(self.player.image, self.player.rect)
        self.brick_group.draw(self.game_ground)
        self.box_group.draw(self.game_ground)
        self.coin_manager.draw(self.game_ground)
        # bilt方法用于把目标图层的特定部分 画到原图层的指定位置
        surface.blit(self.game_ground, (0,0),self.game_window)#目标图层，左上角，特定部分
        self.info.draw(surface)

