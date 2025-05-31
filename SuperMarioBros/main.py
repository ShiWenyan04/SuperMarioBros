#游戏主要入口
import pygame
from source import tools,setup_QiDong
from source.state_YouXiZhuangTai import main_menu,load_screen,level_GuanQia

import threading
import pygame
from pygame import mixer
import time

filepath = r"./resources/music/main_theme.ogg"
mixer.init()

def play_music():


    # 加载音乐
    mixer.music.load(filepath)
    mixer.music.play(start=0.0)

    # 播放时长，没有此设置，音乐不会播放，会一次性加载完
    time.sleep(5) # 360s

    # # 音乐停止播放
    # mixer.music.stop()

def game():
    # 游戏三种状态，主菜单页面，游戏载入状态，游戏关卡状态，
    states = {
        'main_menu': main_menu.MainMenu(),
        # 'load_screen' : load_screen.LoadScreen(),
        'level_GuanQia': level_GuanQia.Level(),
    }
    game = tools.Game(states, 'main_menu')
    game.run()

def main():
    game()
    # # 创建两个线程
    t2 = threading.Thread(target=play_music)
    t1 = threading.Thread(target=game)
    # # 启动两个线程
    # t1.start()
    # t2.start()



if __name__ == '__main__':
    main()