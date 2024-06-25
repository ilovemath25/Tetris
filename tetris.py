import pygame
from src.codeh import Tetris
from src.start import Start
from src.option import Option
pygame.init()
win = pygame.display.set_mode((600,700))
pygame.display.set_caption('Tetris')
run = True
in_start = True
in_game = False
in_option = False
bgm = pygame.mixer.music.load('music/bgm.wav')
gfx_volume = 0.5
bgm_volume = 0.5
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(bgm_volume)
start = Start(gfx_volume)
tetris = Tetris(gfx_volume)
option = Option(gfx_volume, bgm_volume)
score = 0
highscore = 0
level = 0
level_up_score = 100
count = 1
while run:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:run = False
   if in_start:
      start.draw(win)
      start.key()
      run = start.run
      if start.choice == 1 and start.accept:
         in_game = True
         in_start = False
         tetris = Tetris(gfx_volume)
      elif start.choice == 2 and start.accept:
         in_option = True
         in_start = False
         option = Option(gfx_volume, bgm_volume)
      elif start.choice == 3 and start.accept:
         run = False
   if in_option:
      option.draw(win)
      gfx_volume, bgm_volume = option.key()
      pygame.mixer.music.set_volume(bgm_volume)
      run = option.run
      if option.back:
         in_start = True
         in_option = False
         start = Start(gfx_volume)
   if in_game and not(tetris.gameover) and not(tetris.pause):
      tetris.draw(win)
      win.blit(pygame.font.SysFont('comicsan',30,True).render(str(score),1,(255,255,255)),(390,235))
      win.blit(pygame.font.SysFont('comicsan',30,True).render(str(highscore),1,(255,255,255)),(390,295))
      win.blit(pygame.font.SysFont('comicsan',30,True).render(str(level),1,(255,255,255)),(390,355))
      tetris.key()
      tetris.check_row()
      run = tetris.run
      score = tetris.score
      if(score>level_up_score):
         level+=1
         level_up_score+=100
         tetris.falling_delay-=0.3
      if highscore<score:highscore=score
   if tetris.gameover:
      if count:
         win.blit(pygame.image.load("image/pause_bg.png"),(0,0))
         win.blit(pygame.image.load("image/gameover.png"),(0,0))
         pygame.display.update()
         pygame.mixer.music.set_volume(0)
         pygame.mixer.Sound("music/gameover.wav").play()
         pygame.time.delay(2000)
         count=0
         pygame.mixer.music.set_volume(bgm_volume)
      win.blit(pygame.image.load("image/gameover.png"),(0,0))
      if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if(pos[0]in range(218,388))and(pos[1]in range(380,410)):
               count = 1
               tetris.gameover = False
               tetris = Tetris(gfx_volume)
            elif(pos[0]in range(218,388))and(pos[1]in range(435,465)):
               in_start = True
               in_game = False
               tetris.gameover = False
               count = 1
               start = Start(gfx_volume)
      elif event.type == pygame.MOUSEMOTION:
         pos = pygame.mouse.get_pos()
         if(pos[0]in range(218,388))and(pos[1]in range(380,410)):win.blit(pygame.image.load("image/retry.png"),(0,0))
         elif(pos[0]in range(218,388))and(pos[1]in range(435,465)):win.blit(pygame.image.load("image/pause_back.png"),(0,0))
   if tetris.pause:
      if count:
         win.blit(pygame.image.load("image/pause_bg.png"),(0,0))
         count=0
      win.blit(pygame.image.load("image/pause.png"),(0,0))
      if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if(pos[0]in range(218,388))and(pos[1]in range(380,410)):
               tetris.pause = False
               count = 1
            elif(pos[0]in range(218,388))and(pos[1]in range(435,465)):
               in_start = True
               in_game = False
               tetris.pause = False
               count = 1
               start = Start(gfx_volume)
      elif event.type == pygame.MOUSEMOTION:
         pos = pygame.mouse.get_pos()
         if(pos[0]in range(218,388))and(pos[1]in range(380,410)):win.blit(pygame.image.load("image/pause_resume.png"),(0,0))
         elif(pos[0]in range(218,388))and(pos[1]in range(435,465)):win.blit(pygame.image.load("image/pause_back.png"),(0,0))
   pygame.display.update()
pygame.quit()