#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pygame
#导入pygame库
from pygame.locals import *
#导入一些常用的函数和常量
import random
from sys import exit
#向sys模块借一个exit函数用来退出程序

#判断首页，开始界面，游戏界面，失败界面和胜利界面的依据
n0 = 1
n1 = 0
n2 = 0
n3 = 0
n4 = 0

caption_width = 350
caption_height = 700
game_title = '梦云飞飞飞'
#画布尺寸、标题设置

#障碍物尺寸
barrior_width = int(180*0.6)  #141
barrior_height = int(563*0.6)

speed = 6
space = 250

floor_width = caption_width
floor_height = 150

mm_width = int(40*1.3)
mm_height = int(56.6*1.3)
#控制对象的大小

button_width = 100
button_height = 100
#重新开始按钮的大小
start_button_width = 100
start_button_height = 31

score = 0
#分数

pygame.mixer.init()
#加载音乐
pygame.mixer.music.load('music.mp3')

class MM(pygame.sprite.Sprite):
    def __init__(self, top = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('MM.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (mm_width, mm_height))
        self.rect = self.image.get_rect()
        self.rect.left = caption_width/2 - mm_width
        self.rect.top = caption_height / 2 - mm_height - top
        self.speed = speed
        #MM永远在正中间

    def update(self):
        self.speed += 1
        self.rect.top += self.speed
#人物自动下落

    def fly(self):
        self.speed = -speed
#人物向上飞

class Barrior(pygame.sprite.Sprite):
    def __init__(self, change, left, top):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Barrior2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (barrior_width, barrior_height))
        self.rect = self.image.get_rect()
        self.rect.left = left
        if change:
            self.image = pygame.transform.flip(self.image, False, True)
            # pygame.transform.flip(Surface, xbool, ybool)  (水平和垂直翻转)
            self.rect.top = caption_height - top
        else:
            self.rect.top = - (self.rect.bottom - top)
#障碍物上下一起来
    def update(self):
        self.rect.left -= speed*2
#障碍物的更新是障碍物从右向左移动


class Floor(pygame.sprite.Sprite):
    def __init__(self, left):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('cloud.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (floor_width, floor_height))

        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = caption_height - floor_height

#重新开始按钮类
class StartButton(object):
    def __init__(self, upimage, downimage, position):
        self.imageUp = pygame.image.load(upimage).convert_alpha()
        self.imageUp = pygame.transform.scale(self.imageUp, (start_button_width, start_button_height))
        self.imageDown = pygame.image.load(downimage).convert_alpha()
        self.imageDown = pygame.transform.scale(self.imageDown, (start_button_width, start_button_height))
        self.position = position
        self.button_out = True

    def isOver(self):  #判断是否在重新开始按钮上
        point_x, point_y = pygame.mouse.get_pos()
        x, y = self.position
        w, h = button_width, button_height

        in_x = x - w / 2 < point_x < x + w / 2
        in_y = y - h / 2 < point_y < y + h / 2
        return in_x and in_y

    def render(self):
        w, h = button_width, button_height
        x, y = self.position

        if self.isOver():
            caption.blit(self.imageDown, (x - w / 2, y - h / 2))
        else:
            caption.blit(self.imageUp, (x - w / 2, y - h / 2))

#重新开始按钮类
class Button(object):
    def __init__(self, upimage, downimage, position):
        self.imageUp = pygame.image.load(upimage).convert_alpha()
        self.imageUp = pygame.transform.scale(self.imageUp, (button_width, button_height))
        self.imageDown = pygame.image.load(downimage).convert_alpha()
        self.imageDown = pygame.transform.scale(self.imageDown, (button_width, button_height))
        self.position = position
        self.button_out = True

    def isOver(self):  #判断是否在重新开始按钮上
        point_x, point_y = pygame.mouse.get_pos()
        x, y = self.position
        w, h = button_width, button_height

        in_x = x - w / 2 < point_x < x + w / 2
        in_y = y - h / 2 < point_y < y + h / 2
        return in_x and in_y

    def render(self):
        w, h = button_width, button_height
        x, y = self.position

        if self.isOver():
            caption.blit(self.imageDown, (x - w / 2, y - h / 2))
        else:
            caption.blit(self.imageUp, (x - w / 2, y - h / 2))

def generate_Barrior(left):
    top = random.randint(100, 300)
    barrior = Barrior(False, left, top)
    barrior_changed = Barrior(True, left, caption_height - top - space)
    return barrior, barrior_changed

#def go_die():
    #background = pygame.image.load('e:/python/learning/flappymm/gameover.png')
    #background = pygame.transform.scale(background, (caption_width, caption_height))
    #caption.blit(background,(0,0))
    #pygame.display.update()
    #n2 = 0
    #n3 = 1




if __name__ == '__main__':
    pygame.init()
    #初始化pygame，为使用硬件做准备
    game_font = pygame.font.SysFont('arial', 20, True)
    caption = pygame.display.set_mode((caption_width, caption_height))
    pygame.display.set_caption(game_title)

    clock = pygame.time.Clock()

    while True:

        clock.tick(15)

        # 检查音乐流播放，有返回True，没有返回False
        # 如果没有音乐流则选择播放
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()

        background = pygame.image.load('background.png')
        background = pygame.transform.scale(background, (caption_width, caption_height))
        Firstpage = pygame.image.load('Firstpage.jpg')
        Firstpage = pygame.transform.scale(Firstpage, (caption_width, caption_height))
        Secondpage = pygame.image.load('Secondpage.png')
        Secondpage = pygame.transform.scale(Secondpage, (caption_width, caption_height))
        caption.blit(background, (0, 0))

        mm_group = pygame.sprite.Group()
        mm = MM()
        mm_group.add(mm)

        floor_group = pygame.sprite.Group()
        floor = Floor(0)
        floor_group.add(floor)

        barrior_group = pygame.sprite.Group()
        barriors1 = generate_Barrior(300)
        barrior_group.add(barriors1[0])
        barrior_group.add(barriors1[1])

        button = Button('restart1.png', 'restart2.png', (caption_width / 2, caption_height / 2 + 20))
        start_button = StartButton('stratbutton1.png', 'startbutton2.png', (caption_width / 2, caption_height / 2 + 260))

        while n0:
            caption.blit(Firstpage, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                #按下关闭按钮
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                    pygame.time.wait(500)
                    n0 = 0
                    n1 = 1
            pygame.display.update()


        while n1:
            caption.blit(Secondpage, (0, 0))
            start_button.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                #按下关闭按钮
                    pygame.quit()
                    exit()

                if event.type == MOUSEBUTTONDOWN and start_button.isOver():
                    pygame.time.wait(500)
                    n1 = 0
                    n2 = 1
            pygame.display.update()

        while n2:

            clock.tick(15)
            caption.blit(background, (0, 0))
            caption.blit(game_font.render('score:%d' % score, True, [255, 255, 255]), [20, 20])

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE or event.key == K_w or event.key == K_UP:
                        mm.fly()
                if event.type == pygame.QUIT:
                    #按下关闭按钮
                    pygame.quit()
                    exit()

            if barrior_group.sprites()[0].rect.left < -(caption_width): #判断障碍物是否在画布外，是则重新生成障碍物
                barrior_group.remove(barrior_group.sprites())
                barriors = generate_Barrior(caption_width)
                barrior_group.add(barriors[0])
                barrior_group.add(barriors[1])
                score +=1

            mm_group.update()
            mm_group.draw(caption)
            barrior_group.update()
            barrior_group.draw(caption)
            floor_group.draw(caption)

            pygame.display.update()


#碰撞检测
            if pygame.sprite.groupcollide(mm_group, floor_group, False, False)\
                    or pygame.sprite.groupcollide(mm_group, barrior_group, False, False):
                #go_die()
                pygame.time.wait(200)
                n2 = 0
                n3 = 1

#如果通关
            if score > 4:
                pygame.time.wait(200)
                n2 = 0
                n4 = 1
                #print (n1,n2,n3)

            pygame.display.update()
# 刷新画面
            #pygame.quit()
            #exit()

        while n3:
            score = 0
            clock.tick(15)
            background = pygame.image.load('gameover.png')
            background = pygame.transform.scale(background, (caption_width, caption_height))
            caption.blit(background, (0, 0))
            button.render()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                #按下关闭按钮
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN and button.isOver():
                    pygame.time.wait(500)
                    n3 = 0
                    n2 = 1

        while n4:
            score = 0
            clock.tick(15)
            background = pygame.image.load('victory.png')
            background = pygame.transform.scale(background, (caption_width, caption_height))
            caption.blit(background, (0, 0))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 按下关闭按钮
                    pygame.quit()
                    exit()

