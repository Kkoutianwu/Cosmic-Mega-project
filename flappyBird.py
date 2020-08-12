# -*- coding: UTF-8 -*-

#导入pygame库
import pygame
#向sys模块借一个exit函数用来退出程序
from sys import exit
# 导入 random(随机数) 模块
import random
from PIL import Image
import matplotlib.pyplot as plt


FPS = 30 # 帧率
fpsClock = pygame.time.Clock()

#鸟
class Bird(object):
    # 初始化鸟
    def __init__(self, scene):
        # 加载相同张图片资源,做交替实现地图滚动
        self.image = pygame.image.load("src/bird.png")
        # 保存场景对象
        self.main_scene = scene
        # 尺寸
        self.size_x = 80
        self.size_y = 60
        # 辅助移动地图
        self.x = 40
        self.y = 120
 
    # 计算鸟绘制坐标
    def action(self, jump = 4):
        self.y = self.y + jump
        if self.y > 520 :
            self.y = 520
        if self.y < 0 :
            self.y = 0
 
    # 绘制鸟的图片
    def draw(self):
        self.main_scene.scene.blit(self.image, (self.x, self.y))

# 地图
class GameBackground(object):
    # 初始化地图
    def __init__(self, scene):
        # 加载相同张图片资源,做交替实现地图滚动
        self.image1 = pygame.image.load("src/background.jpg")
        self.image2 = pygame.image.load("src/background.jpg")
        # 保存场景对象
        self.main_scene = scene
        # 辅助移动地图
        self.x1 = 0
        self.x2 = self.main_scene.size[1]
        self.speed = 4
        # 柱子图
        self.pillar = pygame.image.load("src/pillar.png")
        # 柱子 宽100 长1000 中间空隙200
        self.pillar_nums = 1
        self.pillar_positions_x = [800] 
        self.pillar_positions_y = [-200] 
 
    # 计算地图图片绘制坐标
    def action(self, addPillar = False):
        # 计算柱子新位置
        for i in range(0, self.pillar_nums):
            self.pillar_positions_x[i] -=  self.speed
        
        if self.pillar_nums > 0 and self.pillar_positions_x[0] + 100 < 0:
            del self.pillar_positions_x[0]
            del self.pillar_positions_y[0]
            self.pillar_nums -= 1

        if addPillar:
            self.pillar_nums += 1
            self.pillar_positions_x.append(800)
            self.pillar_positions_y.append(random.randint(-400, 0)) 

        # 地图
        self.x1 = self.x1 - self.speed
        self.x2 = self.x2 - self.speed
        if self.x1 <= -self.main_scene.size[1]:
            self.x1 = 0
        if self.x2 <= 0:
            self.x2 = self.main_scene.size[1]
 
    # 绘制地图
    def draw(self):
        self.main_scene.scene.blit(self.image1, (self.x1, 0))
        self.main_scene.scene.blit(self.image2, (self.x2, 0))
        for i in range(0, self.pillar_nums):
            self.main_scene.scene.blit(self.pillar, (self.pillar_positions_x[i], self.pillar_positions_y[i]))

# 主场景
class MainScene(object):
    # 初始化主场景
    def __init__(self):
        # 场景尺寸
        self.size = (800, 600)
        # 场景对象
        self.scene = pygame.display.set_mode([self.size[0], self.size[1]])
        # 得分
        self.point = 0
        # 设置标题及得分
        pygame.display.set_caption("Flappy Bird v1.0        得分:" + str(int(self.point)))
        # 暂停
        self.pause = False
        # 创建地图对象
        self.map = GameBackground(self)
        # 创建鸟对象
        self.bird = Bird(self)
        # 输了吗
        self.lose = False

    # 绘制
    def draw_elements(self):
        self.map.draw()
        self.bird.draw()
        pygame.display.set_caption("Flappy Bird v1.0      得分:" + str(float('%.2f' % self.point)))
 
    # 动作
    def action_elements(self, addPillar = False):
        self.map.action(addPillar)
        self.bird.action()
 
    # 处理事件
    def handle_event(self):
        for event in pygame.event.get():
            print(event.type)
            if event.type == 12:
                #接收到退出事件后退出程序
                exit()
            elif event.type == 1:
                #光标移出屏幕
                self.pause = True
            elif event.type == 4:
                 #光标移入屏幕
                self.pause = False
            elif event.type == 5:
                self.bird.action(-60)
            else:
                pass
    
    # 碰撞检测, 碰到返回-1, 过了返回1, 其他0
    def detect_conlision(self):
        # 只要检查第一个柱子
        if self.map.pillar_positions_x[0] <=  self.bird.size_x + self.bird.x and self.map.pillar_positions_x[0] >= -60:
            if self.map.pillar_positions_y[0] + 400 <  self.bird.y and self.bird.y < self.map.pillar_positions_y[0] + 600:
                if self.map.pillar_positions_x[0] == -60:
                    return 1
            else:
                return -1
        return 0

 
    # 主循环,主要处理各种事件
    def run_scene(self):
        #放段音乐听
        pygame.mixer.init()
        pygame.mixer.music.load('src/Jibbs - Chain Hang Low.mp3')
        pygame.mixer.music.play(-1)
        now = 0
        while True:
            # 处理事件
            self.handle_event()
            # 不暂停
            if self.pause == False and self.lose == False:
                # 计算元素坐标
                # 每3秒画个新柱子
                if now == 90:
                    self.action_elements(True)
                    now = 0
                else:
                    self.action_elements(False)
                    now += 1
                # 绘制元素图片
                self.draw_elements()
                # 碰撞检测
                state = self.detect_conlision()
                if state == 1:
                    self.point += 1 
                elif state == -1:
                    pygame.display.set_caption("Flappy Bird v1.0 游戏终止 得分:" + str(float('%.2f' % self.point)))
                    self.lose = True
                    pygame.quit()

                    break
                # 刷新显示
                pygame.display.update()
                fpsClock.tick(FPS)
 
 
# 入口函数
if __name__ == "__main__":
    # 创建主场景
    mainScene = MainScene()
    # 开始游戏
    mainScene.run_scene()
    # 结束游戏后的嘲讽
    pil_im = Image.open('src/你真垃圾.jpg')
    plt.imshow(pil_im)
    plt.ion()
    plt.pause(1)
    plt.close()
