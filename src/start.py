import pygame
class Start:
   def __init__(self,gfx_volume):
      self.run = True
      self.choice = 0
      self.accept = False
      self.pos = []
      self.menu = [[range(150,455),range(300,350)],[range(150,455),range(400,450)],[range(150,455),range(500,550)]]
      self.button_sound = pygame.mixer.Sound("music/button-sound.wav")
      self.button_sound.set_volume(gfx_volume)
   def draw(self,win):
      win.blit(pygame.image.load('image/start.png'),(0,0))
      if self.choice==1:win.blit(pygame.image.load('image/play.png'),(0,0))
      if self.choice==2:win.blit(pygame.image.load('image/option.png'),(0,0))
      if self.choice==3:win.blit(pygame.image.load('image/quit.png'),(0,0))
   def check_mouse_pos(self):
      for checkx,checky in self.menu:
         if (self.pos[0][0] in checkx)and(
            self.pos[0][1] in checky)and(
            self.pos[1][0] in checkx)and(
            self.pos[1][1] in checky):return True
      return False
   def key(self):
      for event in pygame.event.get():
         if event.type == pygame.QUIT:self.run = False
         elif event.type == pygame.MOUSEMOTION:
            xy = pygame.mouse.get_pos()
            if(xy[0] in self.menu[0][0])and(xy[1] in self.menu[0][1]):self.choice = 1
            elif(xy[0] in self.menu[1][0])and(xy[1] in self.menu[1][1]):self.choice = 2
            elif(xy[0] in self.menu[2][0])and(xy[1] in self.menu[2][1]):self.choice = 3
            else:self.choice = 0
         elif event.type == pygame.MOUSEBUTTONDOWN:self.pos.append(pygame.mouse.get_pos())
         elif event.type == pygame.MOUSEBUTTONUP:
            try:
               self.pos.append(pygame.mouse.get_pos())
               if self.check_mouse_pos():
                  self.button_sound.play()
                  self.accept = True
                  self.pos = []
               else:self.pos = []
            except:self.pos = []