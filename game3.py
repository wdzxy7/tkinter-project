# -*- coding=utf-8 -*-
import pygame
from pygame.locals import KEYDOWN
import random


def get_random_word(w):
    color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)) # 颜色随机
    x = random.randint(100, w-100) # x坐标从左右边距各100之间随机
    y = 0
    word = random.randint(65, 90)
    return x, y, word, color


def main():
    w, h = 800, 600
    pygame.init()
    screen = pygame.display.set_mode((w, h))

    white = 255, 255, 255
    black = 0, 0, 0
    myfont = pygame.font.Font(None, 80)

    diff_ticks = 20
    ticks = pygame.time.get_ticks() + diff_ticks
    word_diff_ticks = 1000
    word_ticks = pygame.time.get_ticks() + word_diff_ticks
    arr=[]
    arr.append(get_random_word(w))

    clear_word=0
    level = 1
    pygame.display.set_caption('typing level:%d'%level)
    game_state=1  # 1.进行中 2.游戏失败
    sign=1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_state==1 and len(arr)>0 and event.type == KEYDOWN:
                if event.key == arr[0][2]+32: # 大小写字母差32
                    arr.pop(0)
                    clear_word += 1
                    if clear_word >= level*10:
                        level+=1
                        pygame.display.set_caption('typing level:%d' % level)
                        diff_ticks=diff_ticks*0.9
                        word_diff_ticks=word_diff_ticks*0.95

        screen.fill((255, 255, 255))

        for i in range(len(arr)): # 绘制这些字母
            x, y, word, c = arr[i]
            if i==0 and sign:
                c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            textImage = myfont.render(chr(word), True, c)
            screen.blit(textImage, (x, y))

        if game_state == 2:
            textImage = myfont.render("Level%d fail"%level, True, (255,0,0))
            sw,sh = textImage.get_size()
            screen.blit(textImage, ((w-sw)/2, (h-sh)/2)) # 居中显示

        if game_state == 1:
            if pygame.time.get_ticks()>=word_ticks: # 计时增加新字母
                word_ticks +=word_diff_ticks
                arr.append(get_random_word(w))

            if pygame.time.get_ticks() >= ticks:
                ticks += diff_ticks
                sign=1-sign
                for i in range(len(arr)):
                    x, y, word, c = arr[i]
                    arr[i] = (x, y+1, word, c)
                if len(arr) > 0 and arr[0][1] > h: game_state=2
        pygame.display.update()


