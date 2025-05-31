import pygame
from . import coin_JinBi
import random


class CoinManager:
    def __init__(self):
        self.coin_group = pygame.sprite.Group()
        self.coin_positions = []  # 可以预定义金币位置或随机生成

    def setup_coins(self, positions=None):
        """初始化金币位置"""
        if positions:
            self.coin_positions = positions
        else:
            # 随机生成一些金币位置
            self.coin_positions = [(random.randint(100, 700), random.randint(100, 400))
                                   for _ in range(10)]

        for pos in self.coin_positions:
            self.coin_group.add(coin_JinBi.FlashingCoin(pos[0], pos[1]))

    def update(self):
        self.coin_group.update()

    def draw(self, surface):
        pass
        # self.coin_group.draw(surface)

    def check_collision(self, player):
        """检测玩家与金币的碰撞"""
        coins_collected = pygame.sprite.spritecollide(player, self.coin_group, True)
        for coin in coins_collected:
            coin.collect()
            return True  # 返回是否收集到金币
        return False