import pygame
import sys
import numpy as np
pygame.init()
class main:
    def __init__(self):
        self.monitor = pygame.display.Info() #get the monitor info
        self.screen = pygame.Surface((int((self.monitor.current_w-100)), int((self.monitor.current_h-100)))) #creates a screen used to scale the game up
        self.display = pygame.display.set_mode((self.monitor.current_w-100, self.monitor.current_h-100)) #create a display the size of the monitor

        self.clock = pygame.time.Clock()
        self.angleOne = np.pi/13
        self.angleTwo = -np.pi/2
        self.keys = [0, 0]

        self.center = (self.screen.get_width()//2, self.screen.get_height()//2)

    def run(self):
        while True:
            self.screen.fill((255,255,255))
            height = self.screen.get_height()
            lineOne = [self.center[0]+344*np.cos(self.angleOne), (self.center[1]+344*np.sin(self.angleOne))]
            lineTwo = [lineOne[0]+(310*np.cos(self.angleTwo)), (lineOne[1]+(310*np.sin(self.angleTwo)))]
            lineOne[1] = height - lineOne[1]
            lineTwo[1] = height-lineTwo[1]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.keys[0] = 1
                    if event.key == pygame.K_s:
                        self.keys[1] == 1
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.keys[0] = 0
                    if event.key == pygame.K_s:
                        self.keys[1] == 0
            
            pygame.draw.line(self.screen, (255, 0, 0), self.center, lineOne)
            pygame.draw.line(self.screen, (0, 0, 255), lineOne, lineTwo)

            self.display.blit(pygame.transform.scale(self.screen, (self.display.get_width(), self.display.get_height())), (0, 0))
            pygame.display.update()
            self.clock.tick(30)
main().run()