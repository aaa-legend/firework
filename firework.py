import time

import numpy as np
import pygame
import random
import scipy.io.wavfile as wav


# 定义一个烟花类
class Firework:
    def __init__(self, x, y, color, size):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.exploded = False
        self.falldown = False
        self.acc_x = 5
        self.acc_y_up = 8
        self.acc_y_down = 1
        self.speed = 8 * np.sqrt(self.size / 100)

        self.particles = []


# 在窗口中绘制烟花
def draw_firework(firework):
    if not firework.exploded:
        # 绘制烟花
        for i in range(10):
            pygame.draw.circle(screen, firework.color, (firework.x, firework.y+10* i), 3-i/10*3)

    else:
        # 绘制烟花爆炸后的烟花碎片
        for particle in firework.particles:
            if len(particle[6]) <=20:
                for i in range(len(particle[6])):
                    pygame.draw.circle(screen, particle[2], (particle[6][-i-1][0], particle[6][-i-1][1]), 5 - i / 20 * 5)
            else:
                for i in range(20):
                    pygame.draw.circle(screen, particle[2], (particle[6][-i-1][0], particle[6][-i-1][1]), 5 - i/20*5)
            # pygame.draw.circle(screen, particle[2], (particle[0], particle[1]), 2)



# 更新烟花状态
def update_firework(firework):
    if not firework.exploded:
        # 烟花升高
        high = random.randint(100, 200)
        firework.y -= 12
        # 如果烟花升到顶部，则触发爆炸
        if firework.y < high:
            firework.exploded = True
            firework.y = high
            # 为烟花爆炸创建烟花碎片
            for i in range(firework.size):
                angle = random.uniform(0, 2* np.pi)
                angle1 = random.uniform(0, np.pi/2)
                speed_x = firework.speed * np.cos(angle) * np.cos(angle1)
                speed_y = firework.speed * np.sin(angle) * np.cos(angle1)
                local =[]
                t = 0
                particle = [firework.x, firework.y, firework.color, speed_x, speed_y, angle, local, t]
                firework.particles.append(particle)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(fileworkpath))
    else:
        # 烟花爆炸后的
        if not firework.falldown:
            for particle in firework.particles:
                if particle[5] < np.pi/2 or particle[5] > np.pi * 1.5:
                    if particle[3] > 0:
                        particle[3] = particle[3] - firework.acc_x / fps
                    else:
                        particle[3] = 0
                elif np.pi/2 < particle[5] < np.pi * 1.5:
                    if particle[3] < 0:
                        particle[3] = particle[3] + firework.acc_x / fps
                    else:
                        particle[3] = 0
                else:
                    particle[3] = 0
                if 0< particle[5] < np.pi:
                    particle[4] = particle[4] - firework.acc_y_up / fps
                else:
                    particle[4] = particle[4] - firework.acc_y_down / fps
                # particle[4] = particle[4] - firework.acc_y / fps

                particle[0] += particle[3]
                particle[1] -= particle[4]
                particle[6].append([particle[0], particle[1]])
                particle[7] += 1

def dropfirework(fireworks):
    for firework in fireworks:
        if firework.exploded:
            if firework.particles[0][7] > 35:
                fireworks.remove(firework)


if __name__ == '__main__':
    # 初始化 Pygame
    pygame.init()

    # 设置窗口大小和标题
    width = 1920
    height = 1080
    screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
    pygame.display.set_caption('Fireworks Show')

    # 加载背景图片
    bg_image = pygame.image.load('backgroundimg.jpg')

    # pygame.display.set_caption("Alien Invasion")
    fcclock = pygame.time.Clock()
    fps = 30
    fireworks = []
    running = True
    filename = "music.wav"
    fileworkpath = "boom.mp3"
    fs,signal = wav.read(filename)
    signal[:,0] = abs(signal[:,0])
    t_legth = signal.shape[0] / fs
    a = []
    for i in range(int(t_legth)):
        a.append(np.mean(signal[i*fs:(i+1)*fs, 0])) #根据fps对音频的振幅进行均值采样
    
    pygame.mixer.init()
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(filename))

    t = 0

    while running:
    # 绘制背景
        screen.blit(pygame.transform.scale(bg_image, (width,height)), (0, 0))
    # 处理事件
        t += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                size = width, height = event.size[0], event.size[1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标单击时创建新烟花
                x, y = pygame.mouse.get_pos()
                color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                size = random.randint(50, 150)
                firework = Firework(x, height, color, size)
                fireworks.append(firework)
        if t%fps == 0 and t/fps <= len(a)-2:
            print(t/fps)
            delay = 1
            for i in range(int(a[int(t/fps)+delay]/1000)):  #根据音乐的振幅大小判断烟花数量,delay为烟花提前出现的时间，除以1000来控制烟花的数量

                rand_x = random.randint(0, width)
                rand_y = random.randint(height-100, height)
                color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                size = random.randint(50, 150)
                firework = Firework(rand_x, rand_y, color, size)
                fireworks.append(firework)

        # 更新和绘制烟花
        for firework in fireworks:
            update_firework(firework)
            draw_firework(firework)
        dropfirework(fireworks)

        # 更新屏幕
        fcclock.tick(fps)

        pygame.display.update()
    pygame.quit()