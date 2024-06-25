import pygame
import random
import time
listblock = ["i","j","l","o","s","t","z"]
random.shuffle(listblock)
grid = [[[51+30*c,51+30*r] for c in range(10)] for r in range(20)]
class Block:
   def __init__(self,next,x,y) -> None:
      self.x = x
      self.y = y
      self.rotate = 0
      self.width = 0
      self.height = 0
      self.pos = []
      if(next>6):next = random.randint(0,6)
      self.shape = listblock[next]
      self.status = True      
class Tetris:
   def identify(self,shape,rotate,x,y):
      if(shape == 'i'):
         width = 30;height = 120
         pos = [[x,y],[x,y+30],[x,y+60],[x,y+90]]
         color = (61,180,254)
         if(rotate%2==0):
            width = 30;height = 120
            pos = [[x,y],[x,y+30],[x,y+60],[x,y+90]]
         elif(rotate%2==1):
            width = 120;height = 30
            pos = [[x,y],[x+30,y],[x+60,y],[x+90,y]]
      elif(shape == 'j'):
         width = 90;height = 60
         pos = [[x+60,y],[x+60,y+30],[x,y+30],[x+30,y+30]]
         color = (236,133,0)
         if(rotate%4==0):
            width = 90;height = 60
            pos = [[x+60,y],[x+60,y+30],[x,y+30],[x+30,y+30]]
         elif(rotate%4==1):
            width = 60;height = 90
            pos = [[x,y],[x,y+30],[x,y+60],[x+30,y+60]]
         elif(rotate%4==2):
            width = 90;height = 60
            pos = [[x,y],[x+30,y],[x+60,y],[x,y+30]]
         elif(rotate%4==3):
            width = 60;height = 90
            pos = [[x+30,y],[x+30,y+30],[x+30,y+60],[x,y]]
      elif(shape == 'l'):
         width = 90;height = 60
         pos = [[x, y],[x, y+30],[x+30, y+30],[x+60, y+30]]
         color = (50,50,200)
         if(rotate%4==0):
            width = 90;height = 60
            pos = [[x, y],[x, y+30],[x+30, y+30],[x+60, y+30]]
         elif(rotate%4==1):
            width = 60;height = 90
            pos = [[x,y],[x,y+30],[x,y+60],[x+30,y]]
         elif(rotate%4==2):
            width = 90;height = 60
            pos = [[x,y],[x+30,y],[x+60,y],[x+60,y+30]]
         elif(rotate%4==3):
            width = 60;height = 90
            pos = [[x+30,y],[x+30,y+30],[x+30,y+60],[x,y+60]]
      elif(shape == 'o'):
         width = 60;height = 60
         pos = [[x, y],[x, y+30],[x+30, y+30],[x+30, y]]
         color = (255,200,0)
      elif(shape == "s"):
         color = (0,160,0)
         if(rotate%2==0):
            width = 90;height = 60
            pos = [[x+30,y],[x+60,y],[x,y+30],[x+30,y+30]]
         elif(rotate%2==1):
            width = 60;height = 90
            pos = [[x,y],[x,y+30],[x+30,y+30],[x+30,y+60]]
      elif(shape == "t"):
         color = (120,0,200)
         if(rotate%4==0):
            width = 90;height = 60
            pos = [[x+30,y],[x,y+30],[x+30,y+30],[x+60,y+30]]
         elif(rotate%4==1):
            width = 60;height = 90
            pos = [[x,y],[x,y+30],[x,y+60],[x+30,y+30]]
         elif(rotate%4==2):
            width = 90;height = 60
            pos = [[x+30,y+30],[x,y],[x+30,y],[x+60,y]]
         elif(rotate%4==3):
            width = 60;height = 90
            pos = [[x+30,y],[x+30,y+30],[x+30,y+60],[x,y+30]]
      elif(shape == "z"):
         color = (200,0,0)
         if(rotate%2==0):
            width = 90;height = 60
            pos = [[x, y],[x+30, y],[x+30, y+30],[x+60, y+30]]
         elif(rotate%2==1):
            width = 60;height = 90
            pos = [[x+30,y],[x,y+30],[x+30,y+30],[x,y+60]]
      return width,height,pos,color
   def shapedraw(self,win,block):
      shape = block.shape
      rotate = block.rotate
      x = block.x
      y = block.y
      if block.status:width,height,pos,color = self.identify(shape,rotate,x,y)
      else:
         width,height,_,color = self.identify(shape,rotate,x,y)
         pos = block.pos
      for i in pos:pygame.draw.rect(win,color,(i[0],i[1],27,27))
      return width,height,pos
   def __init__(self,gfx_volume):
      self.deadblock = []
      self.deadcord = []
      self.run = True
      self.block = Block(random.randint(0,12),171,51)
      self.nextblock = 0
      self.nextblockz = Block(self.nextblock,411,111)
      if self.nextblockz.shape=='i':self.nextblockz.rotate+=1
      elif self.nextblockz.shape=='o':self.nextblockz.x+=30
      self.second_before = 1
      self.fall_delay = 0.08
      self.last_fall_time = time.time()
      self.falling_delay = 1
      self.score = 0
      self.gameover = False
      self.pause = False
      self.select_pause = False
      self.hit_sound = pygame.mixer.Sound("music/hit.wav")
      self.hit_sound.set_volume(gfx_volume)
      self.row_sound = pygame.mixer.Sound("music/row.wav")
      self.row_sound.set_volume(gfx_volume)
      self.button_sound = pygame.mixer.Sound("music/button-sound.wav")
      self.button_sound.set_volume(gfx_volume)
   def removeline(self,g):
      for gblock in g:self.deadcord.remove(gblock)
      for dblock in self.deadblock:
         for gblock in g:
            try:dblock.pos.remove(gblock)
            except:pass
   def fallline(self, g):
      for dcord in self.deadcord:
         if dcord[1]<g[0][1]:dcord[1]+=30
         else:pass
   def check_row(self):
      line_clear = False
      for g in grid:
         if all(x in self.deadcord for x in g):
            self.removeline(g)
            self.fallline(g)
            line_clear = True
            self.score+=10
      if line_clear:
         self.row_sound.play()
         self.row_sound.play()
         line_clear = False
      if any(dcord[1]<111 for dcord in self.deadcord):
         self.gameover=True
   def hit(self,position):
      if self.block.y + self.block.height == 651:return True
      for pos in position:
         for dcord in self.deadcord:
            if((pos[0]==dcord[0])and(pos[1]==dcord[1]-30)):return True
      return False
   def fall(self):
      if (time.time()-self.last_fall_time)>=self.falling_delay:
         self.block.y += 30
         self.last_fall_time = time.time()
   def draw(self,win):
      win.blit(pygame.image.load('image/bg.jpg'),(0,0))
      self.block.width,self.block.height,self.block.pos = self.shapedraw(win,self.block)
      self.shapedraw(win,self.nextblockz)
      if self.select_pause:win.blit(pygame.image.load('image/pause_button.png'),(0,0))
      if not(self.hit(self.block.pos)):self.fall()
      else:
         self.hit_sound.play()
         self.block.status = False
         self.deadblock.append(self.block)
         for pos in self.block.pos:self.deadcord.append(pos)
         self.block = Block(self.nextblock,171,51)
         self.nextblock+=1
         if self.nextblock>6:
            self.nextblock=0
            random.shuffle(listblock)
         self.nextblockz = Block(self.nextblock,411,111)
         if self.nextblockz.shape=='i':self.nextblockz.rotate+=1
         elif self.nextblockz.shape=='o':self.nextblockz.x+=30
      for dblock in self.deadblock:self.shapedraw(win,dblock)
      if(self.block.x<=51):self.block.x = 51
      elif(self.block.x + self.block.width >= 351):self.block.x = 351 - self.block.width
   def key(self):
      current_time = time.time()
      keys = pygame.key.get_pressed()
      if keys[pygame.K_DOWN] or keys[pygame.K_s]and(not(self.hit(self.block.pos))):
         if current_time - self.last_fall_time >= self.fall_delay:
            self.block.y+=30
            _,_,position,_ = self.identify(self.block.shape,self.block.rotate,self.block.x,self.block.y)
            self.last_fall_time = current_time
      for event in pygame.event.get():
         if event.type == pygame.QUIT:self.run = False
         elif event.type == pygame.KEYDOWN:
            if((event.key == pygame.K_UP)or(event.key == pygame.K_w)):
               self.block.rotate+=1
               _,_,position,_ = self.identify(self.block.shape,self.block.rotate,self.block.x,self.block.y)
               if(self.hit(position)):self.block.rotate-=1
            if((event.key == pygame.K_LEFT)or(event.key == pygame.K_a))and(not(self.block.x <= 51)):
               self.block.x-=30
               _,_,position,_ = self.identify(self.block.shape,self.block.rotate,self.block.x,self.block.y)
               if(self.hit(position)):self.block.x+=30
            elif((event.key == pygame.K_RIGHT)or(event.key == pygame.K_d))and(not(self.block.x + self.block.width >= 351)):
               self.block.x+=30
               _,_,position,_ = self.identify(self.block.shape,self.block.rotate,self.block.x,self.block.y)
               if(self.hit(position)):self.block.x-=30
         elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            if(pos[0]in range(380,560))and(pos[1]in range(590,620)):self.select_pause = True
            else:self.select_pause=False
         elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if(pos[0]in range(380,560))and(pos[1]in range(590,620)):
               self.pause = True
               self.button_sound.play()
if __name__=='__main__':
   for line in grid:print(line)