import pygame

from ..import tools,setup_QiDong
from.. import constants_ChangLiang as C
import json
import os



class Player(pygame.sprite.Sprite):
    def __init__(self,name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.load_data()
        self.setup_States()
        self.setup_velocities()
        self.setup_timers()
        self.load_images()

        self.frame_index=0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.load_sounds()



    # 解析json文件
    def load_data(self):
        file_name = self.name + ".json"
        file_path = os.path.join('source/data/player',file_name)
        with open(file_path) as f:
            self.player_data = json.load(f)

    # 马里奥的状态：是否脸朝右，是否变大，是否死亡无敌等
    def setup_States(self):
        self.state = 'stand'
        self.face_right = True
        self.big = False
        self.dead = False

    # 马里奥的速度,向前后移动距离
    def setup_velocities(self):
        speed = self.player_data['speed']
        self.x_vel = 0
        self.y_vel = 0

        self.max_walk_vel  = speed['max_walk_speed']
        self.max_run_vel = speed['max_run_speed']
        self.max_y_vel = speed['max_y_velocity']
        self.jump_vel = speed['jump_velocity']
        self.walk_accel = speed['walk_accel']
        self.run_accel = speed['run_accel']
        self.turn_accel = speed['turn_accel']
        self.gravity = C.GRAVITY

        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel


    # 计时器，比如马里奥变大的时间
    def setup_timers(self):
        self.walking_timer = 0
        self.transition_timer =0


    # 马里奥的图片
    def load_images(self):
        sheet = setup_QiDong.GRAPHICS['mario_bros']
        frame_rects = self.player_data['image_frames']

        # 定义状态列表 右小 、左小、右大、左大
        self.right_small_normal_frames = []
        self.left_small_normal_frames = []
        self.right_big_normal_frames = []
        self.left_big_normal_frames = []

        # 大小的状态包含左右两种
        self.small_normal_frames = [self.right_small_normal_frames, self.left_small_normal_frames]
        self.big_normal_frames = [self.right_big_normal_frames, self.left_big_normal_frames]

        # 全体的集合
        self.all_frames = [
            self.right_small_normal_frames,
            self.left_small_normal_frames,
            self.right_big_normal_frames,
            self.left_big_normal_frames,
        ]
        # 左右帧库
        self.right_frames = self.right_small_normal_frames
        self.left_frames = self.left_small_normal_frames


        for group,group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
            # 获取四种方向的图片，上下左右
                right_image = tools.get_image(sheet,frame_rect['x'],frame_rect['y'],
                                              frame_rect['width'] ,frame_rect['height'],(0,0,0),C.PLAYER_MULTI)
                left_image = pygame.transform.flip(right_image,True,False)#马里奥镜像向左
                # 小马里奥
                if group == 'right_small_normal':
                    self.right_small_normal_frames.append(right_image)
                    self.left_small_normal_frames.append(left_image)
                # 大玛利奥
                if group == 'right_big_normal':
                    self.right_big_normal_frames.append(right_image)
                    self.left_big_normal_frames.append(left_image)


        self.frame_index = 0 # 第一张动作图索引
        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()


    def update(self,keys):
        self.current_time = pygame.time.get_ticks()
        self.handle_states(keys)

    def handle_states(self,keys):
        if self.state == 'walk':
            self.walk (keys)
        elif self.state == 'stand':
            self.stand(keys)
        elif self.state == 'jump' :
            self.jump(keys)
        elif self.state == ('fall'):
            self.fall(keys)


        if self.face_right:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]


    # 站立，速度统统为0
    def stand(self, keys):
        self.x_vel = 0
        self.y_vel = 0
        self.frame_index = 0
        # 按下左右键，由站立状态转为行走状态，朝向与按下的键有关
        if keys[pygame.K_LEFT]:
            self.face_right = False
            self.state = 'walk'
        elif keys[pygame.K_RIGHT]:
            self.face_right = True
            self.state = 'walk'
        elif keys[pygame.K_SPACE] :
            self.state = 'jump'
            self.can_jump = False
            self.y_vel = self.jump_vel


    # 行走
    def walk(self, keys):
        # 设最大的速度和加速度为步行的最大速度和最大加速度
        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel

        # 行进中的跳跃
        if keys[pygame.K_SPACE]:
            self.state = 'jump'
            self.y_vel = self.jump_vel
            if self.y_vel > self.jump_vel:
                self.state = 'fall'


    #     步行帧切换,在frames中 123为运动状态
        if self.current_time - self.walking_timer > 0.001:
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time

        #     步行中按下右键，第一种为加速状态，第二中为刹车状态
        if keys[pygame.K_RIGHT]:
            self.face_right = True
            if self.x_vel < 0:
                self.frame_index = 5#表示刹车帧
                self.x_accel = self.turn_accel
            #     向右行走，不能超过最大速度，所以为min
            self.x_vel = min(self.x_vel+self.x_accel, self.max_x_vel)
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            if self.x_vel > 0:
                self.frame_index = 5  # 表示刹车帧
                self.x_accel = self.turn_accel
            #     向左行走，同样不能超过最大速度，由于是反方向加符号，所应应该用max
            self.x_vel = max(self.x_vel-self.x_accel, -self.max_x_vel)

        else:#什么键都不按，自动停下来，并且是站立状态
            if self.face_right:
                self.x_vel = 0
                self.frame_index = 0
                self.x_accel = self.turn_accel
            else:
                self.x_vel = 0
                self.frame_index = 0
                self.x_accel = self.turn_accel

    def jump(self, keys):
        self.frame_index = 4
        self.y_vel += self.gravity
        if self.y_vel >= 0:
           self.state = 'fall'
        #   如果在空中左右移动
        if keys[pygame.K_RIGHT]:
            self.x_val = min(self.x_vel+self.x_accel, self.max_x_vel)
        elif keys[pygame.K_LEFT]:
            self.x_val = max(self.x_vel-self.x_accel, -self.max_x_vel)

    def fall(self,keys):
        self.frame_index = 4
        self.y_vel = min(self.y_vel+self.gravity, self.max_y_vel)
        #   如果在空中左右移动
        if keys[pygame.K_RIGHT]:
            self.x_val = min(self.x_vel + self.x_accel, self.max_x_vel)
        elif keys[pygame.K_LEFT]:
            self.x_val = min(self.x_vel - self.x_accel, -self.max_x_vel)

    def load_sounds(self):
        """加载音效"""
        self.sound = pygame.mixer.Sound('./resources/music/main_theme.ogg')

    def collect_coin(self):
        """收集金币时调用"""
        self.sound.play()