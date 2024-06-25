import pygame
class Bar:
    def __init__(self,volume):
        self.x = (volume*490)+60
        self.volume = volume
class Option:
    def __init__(self,gfx_volume, bgm_volume):
        self.dragging = False
        self.choice = 0
        self.gfx = Bar(gfx_volume)
        self.bgm = Bar(bgm_volume)
        self.run = True
        self.back = False
        self.back_button = False
        self.button_sound = pygame.mixer.Sound("music/button-sound.wav")
        self.button_sound.set_volume(gfx_volume)
    def draw(self,win):
        win.blit(pygame.image.load("image/option_bg.jpg"),(0,0))
        if self.gfx.x<60:self.gfx.x=60
        elif self.gfx.x>550:self.gfx.x=550
        if self.bgm.x<60:self.bgm.x=60
        elif self.bgm.x>550:self.bgm.x=550
        pygame.draw.rect(win,(255,200,0),(50,290,self.gfx.x-40,40),border_radius=20)
        pygame.draw.rect(win,(255,200,0),(50,410,self.bgm.x-40,40),border_radius=20)
        win.blit(pygame.image.load("image/option_button.png"),(self.gfx.x-40,280))
        win.blit(pygame.image.load("image/option_button.png"),(self.bgm.x-40,400))
        if(self.back_button):win.blit(pygame.image.load("image/back.png"),(0,0))
    def key(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:self.run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x in range(60,550) and mouse_y in range(290,330):
                        self.dragging = True
                        self.choice = 1
                        self.gfx.offset_x = mouse_x - self.gfx.x
                    elif mouse_x in range(60,550) and mouse_y in range(410,450):
                        self.dragging = True
                        self.choice = 2
                        self.bgm.offset_x = mouse_x - self.bgm.x
                    else:self.choice = 0
                    if mouse_x in range(30,170) and mouse_y in range(625,670):
                        self.back = True
                        self.button_sound.play()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
                    self.choice = 0
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.dragging:
                    if self.choice == 1:
                        if self.gfx.x<60:self.gfx.x=60
                        elif self.gfx.x>550:self.gfx.x=550
                        else:
                            self.gfx.x = mouse_x - self.gfx.offset_x
                            self.gfx.volume = (mouse_x-60)/490
                    elif self.choice == 2:
                        if self.bgm.x<60:self.bgm.x=60
                        elif self.bgm.x>550:self.bgm.x=550
                        else:
                            self.bgm.x = mouse_x - self.bgm.offset_x
                            self.bgm.volume = (mouse_x-60)/490
                if mouse_x in range(30,170) and mouse_y in range(625,670):self.back_button = True
        return self.gfx.volume,self.bgm.volume