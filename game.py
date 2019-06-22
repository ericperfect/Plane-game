# coding=utf-8
import pygame
import time
import random
import sys

from pygame.locals import *


class Plane(object):

    def __init__(self, screen):
        # 设置要显示内容的窗口
        self.screen = screen
        self.image = pygame.image.load(self.imageName).convert()
        # 用来存储英雄飞机发射的子弹
        self.bulletList = []
        self.isDead = False
        # 爆炸效果用的如下属性
        self.hit = False  # 表示是否要爆炸
        self.bomb_list = []  # 用来存储爆炸时需要的图片
        self.image_num = 0  # 用来记录while True的次数,当次数达到一定值时才显示一张爆炸的图,然后清空,当这个次数再次达到时,再显示下一个爆炸效果的图片
        self.image_index = 0  # 用来记录当前要显示的爆炸效果的图片的序号
        self.create_images()  
    def display(self):
         # 显示子弹
        for bullet in self.bulletList:
            bullet.display()
            bullet.move()

        # 存放需要删除的子弹列表
        needRemove = []

        # 判断子弹位置
        for i in self.bulletList:
            if i.judge():
                needRemove.append(i)
        # 删除子弹
        for i in needRemove:
            self.bulletList.remove(i)

        del needRemove

        # 如果被击中,就显示爆炸效果,否则显示普通的飞机效果

        if self.hit == True:
            self.screen.blit(
                self.bomb_list[self.image_index], (self.x, self.y))
            self.image_num += 1
            if self.image_num == 7:
                self.image_num = 0
                self.image_index += 1
            if self.image_index > 3:
                self.isDead = True
        else:
            self.screen.blit(self.image, (self.x, self.y))

    def bomb(self):
        self.hit = True
   

class HeroPlane(Plane):

    def __init__(self, screen):
        # 设置飞机默认位置
        self.x = 190
        self.y = 520
        # 设置要显示内容的窗口
        self.imageName = "./feiji/hero.gif"
        super().__init__(screen)
       # 调用这个方法向bomb_list中添加图片


    def create_images(self):
        self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n1.png"))
        self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n2.png"))
        self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n3.png"))
        self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n4.png"))

    def moveLeft(self):
        if self.x > 0:
            self.x -= 10

    def moveRight(self):
        if self.x < 480 - 100:
            self.x += 10

    def moveUp(self):
        # 判断是否越界
        if self.y > 0:
            self.y -= 10

    def moveDown(self):
        if self.y < 700 - 124:
            self.y += 10

    def shot(self):
        newBullet = Bullet(self.screen, self.x, self.y)
        self.bulletList.append(newBullet)


class EnemyPlane(Plane):
    score = 0

    @classmethod
    def getScore(cls):
        cls.score += 100


    def __init__(self, screen):
        # 设置飞机默认位置
        self.x = 0
        self.y = 0
        
        # 设置要显示内容的窗口
        self.imageName = "./feiji/enemy-1.gif"
        super().__init__(screen)
        # 用来存储英雄飞机发射的子弹
        self.direction = "right"
       
      

    # def __del__(self):
    #     EnemyPlane.getScore()

    def create_images(self):
        self.bomb_list.append(pygame.image.load("./feiji/enemy0_down1.png"))
        self.bomb_list.append(pygame.image.load("./feiji/enemy0_down2.png"))
        self.bomb_list.append(pygame.image.load("./feiji/enemy0_down3.png"))
        self.bomb_list.append(pygame.image.load("./feiji/enemy0_down4.png"))

    
    def move(self):
        if self.direction == "right":
            self.x += 2
        elif self.direction == "left":
            self.x -= 2

        if self.x > 480-50:
            self.direction = "left"
        elif self.x < 0:
            self.direction = "right"

    def shot(self):
        num = random.randint(50, 88)
        if num == 88:
            newBullet = EnemyBullet(self.screen, self.x, self.y)
            self.bulletList.append(newBullet)

    

class Bullet(object):

    def __init__(self, screen, x, y):
        self.x = x + 40
        self.y = y - 20
        self.imageName = "./feiji/bullet-3.gif"
        self.image = pygame.image.load(self.imageName).convert()
        self.screen = screen

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y -= 3

    def judge(self):
        if self.y < 0:
            return True
        else:
            return False


class EnemyBullet(object):

    def __init__(self, screen, x, y):
        self.x = x + 22
        self.y = y + 30
        self.imageName = "./feiji/bullet-1.gif"
        self.image = pygame.image.load(self.imageName).convert()
        self.screen = screen

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += 2

    def judge(self):
        if self.y > 600:
            return True
        else:
            return False

if __name__ == "__main__":
    # 初始化pygame,为使用硬件做准备
    pygame.init()
    # 1创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((480, 700), 0, 32)
    # 2创建一个和窗口大小的图片，用来充当背景
    background = pygame.image.load("./feiji/background.png").convert()
    # 3创建一个飞机对象
    heroPlane = HeroPlane(screen)
    # 4创建一个敌人飞机对象
    enemyPlane = EnemyPlane(screen)
    # 5创建字体对象
    myfont = pygame.font.SysFont('arial', 20, True)
    blue = 0, 0, 200

    while True:
        # 设定需要显示的背景图
        screen.blit(background, (0, 0))
        # 设置窗口标题
        pygame.display.set_caption("飞机大战")
        textImage = myfont.render("Score:" + str(EnemyPlane.score), True, blue)
        screen.blit(textImage, (0, 100))

        heroPlane.display()
        enemyPlane.display()
        enemyPlane.shot()
        enemyPlane.move()
        # 判断敌方飞机是否爆炸完
        if enemyPlane.isDead:
            del enemyPlane
            EnemyPlane.getScore()
            enemyPlane = EnemyPlane(screen)
        # 判断子弹是否击中敌机
        for i in heroPlane.bulletList:
            if enemyPlane.x+51 > i.x and enemyPlane.x < i.x+20 and enemyPlane.y+39 > i.y:
                enemyPlane.bomb()
                
        # 判断我方飞机是否爆炸完
        if heroPlane.isDead:
            del heroPlane
            exit()
        #    heroPlane = HeroPlane(screen)
        # 判断子弹是否击中我方飞机
        for i in enemyPlane.bulletList:
            if heroPlane.x+100 > i.x and heroPlane.x < i.x+9 and heroPlane.y < i.y+21:
                heroPlane.bomb()

        # 获取事件，比如按键等
        for event in pygame.event.get():

            # 判断是否是点击了退出按钮
            if event.type == QUIT:
                print("exit")
                exit()
                sys.exit()
            # 判断是否是按下了键
            elif event.type == KEYDOWN:
                # 检测按键是否是a或者left
                if event.key == K_a or event.key == K_LEFT:
                    print('left')
                    heroPlane.moveLeft()

                # 检测按键是否是d或者right
                elif event.key == K_d or event.key == K_RIGHT:
                    print('right')
                    heroPlane.moveRight()

                elif event.key == K_w or event.key == K_UP:
                    print('up')
                    heroPlane.moveUp()

                elif event.key == K_s or event.key == K_DOWN:
                    print('down')
                    heroPlane.moveDown()
                # 检测按键是否是空格键
                elif event.key == K_SPACE:
                    print('space')
                    heroPlane.shot()

        pygame.display.update()
        # 优化代码
        time.sleep(0.01)
