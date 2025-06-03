#游戏主要入口

from source import tools
from source.state_YouXiZhuangTai import main_menu,level_GuanQia

def game():
    # 游戏三种状态，主菜单页面，游戏载入状态，游戏关卡状态，
    states = {
        'main_menu': main_menu.MainMenu(),
        'level_GuanQia': level_GuanQia.Level(),
    }
    game = tools.Game(states, 'main_menu')
    game.run()

def main():
    game()

if __name__ == '__main__':
    main()