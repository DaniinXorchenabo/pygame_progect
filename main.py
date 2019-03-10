# -*- coding: utf8 -*-
# https://icons8.com/animizer/ru/gif-apng-converter - аниматор
from numpy import*
import pygame
from time import sleep, time
from math import pi, degrees
from random import choice,randrange
import importlib


class AnimatedSprite(pygame.sprite.Sprite):
    
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
 
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
 
    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        

class Particle(pygame.sprite.Sprite):
    osn_object = '-'
    fire = [pygame.image.load("1/destr_1.png"),
            pygame.image.load("1/destr_2.png"),
            pygame.image.load("1/destr_3.png"),
            pygame.image.load("1/destr_4.png"),
            pygame.image.load("1/destr_5.png"),
            pygame.image.load("1/destr_6.png"),
            pygame.image.load("1/destr_7.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[1], (scale, scale)))
        fire.append(pygame.transform.scale(fire[2], (scale, scale)))
        fire.append(pygame.transform.scale(fire[5], (scale, scale)))
        fire.append(pygame.transform.scale(fire[6], (scale, scale)))
 
    def __init__(self, pos, dx, dy, radius, alpha, right):
        super().__init__(prticles)
        self.img = choice(self.fire)
        self.image = pygame.transform.rotate(self.img, randrange(0,360))
        self.rect = self.image.get_rect()
        self.radius = radius + choice(range(-50,50))
        self.alpha = alpha + choice(range(-7,7))/100
        self.d_alpha = ((0.02*self.radius/radius)+0.02)/2
        self.rect.center = pos
        self.mask = pygame.mask.from_surface(self.image)
        self.radius_down = 0
        self.right = right

    def update(self):
        self.alpha += self.d_alpha * self.right
        x = self.radius * cos(self.alpha) + 500 - 60
        pep8_mat = Missiles.osn_object.start_fon_position_for_y + 420 - 44
        y = self.radius * sin(self.alpha) + 1400 + pep8_mat
        self.image = self.img  
        
        self.image1 = pygame.transform.rotate(self.image,
                                              -degrees(self.alpha)*self.right)
        self.mask = pygame.mask.from_surface(self.image1)
        self.rect = self.image1.get_rect()
        self.rect.center = x, y + (0 if sin(self.alpha) < 0 else 2000)
        
        if self.radius < 830:
            self.radius_down += 1
        if self.radius < 300:
            self.kill()
        if self.radius_down != 0:
            if self.radius_down >170:
                self.kill()
            self.radius -= self.radius_down/10
            self.radius_down -= self.radius_down/10 

    def osn_object_function(self, obj):
        Missiles.osn_object = obj     


class Missiles(pygame.sprite.Sprite):
    masshtab = 50
    value = 2000
    group_parts = '-'

    def __init__(self, group,cell0,cell1,pul_tupe, Smax=250):
        super().__init__(group)
        self.pul_tupe = pul_tupe - 1
        self.mass_sprites = [(pygame.image.load("1/pul1_1.png"), (1, 1,)),
                             (pygame.image.load("1/pul_a.png"), (5, 1,)),
                             (pygame.image.load("1/pul_a2.png"), (3, 3,))]
        x0, y0 = self.create_pul(cell0, cell1)
        self.create_tuman()
        self.rect = self.image.get_rect(center=(x0, y0))
        self.coord_c = self.rect.center
        
        dx, dy = (self.x1 - x0), (self.y1 - y0)
        s = (dx ** 2 + dy ** 2) ** 0.5
        self.vx = (15 * (abs(dx)/s))
        self.vy = (15 * (abs(dy)/s))
        self.alpha = arcsin(dx/s)
        if s > Smax:
            s = Smax    
        self.Smax = Smax
        self.stop_time = s/15
        self.ch = 0
        if dx < 0:
            self.vx *= -1
        if dy < 0:
            self.vy *= -1
        if dy > 0:
            if dx > 0:
                self.right = -1
                um = 180
            else:
                self.right = -1
                um = 180
        else:
            self.right = 1
            um = 0
        self.degrees_rotare = -degrees(self.alpha) * self.right - um
        self.img = pygame.transform.rotate(self.img, self.degrees_rotare)
        self.tuman = pygame.transform.rotate(self.tuman, self.degrees_rotare)
        self.width, self.height = self.rect.size
        self.become_tuman = Missiles.masshtab
        self.image = self.img
        try:
            self.y0_fon = abs(self.osn_play.start_fon_position_for_y)
        except Exception as e:
            print('erorr ', e)
            self.y0_fon = 1700

    def create_osn_class(self, osn_play):
        self.osn_play = osn_play
        #print('------', self.y0_fon)

    def create_pul(self, cell0, cell1):
        x0, y0 = cell0
        self.x1, self.y1 = cell1
        self.frames = []
        pep8_mn = self.mass_sprites[self.pul_tupe][1]
        self.cut_sheet(self.mass_sprites[self.pul_tupe][0], * pep8_mn)
        self.cur_frame = 0
        self.img = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.img)
        self.image = self.img
        return x0, y0

    def cut_sheet(self, sheet, columns, rows):
        self.rect1 = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect1.w * i, self.rect1.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect1.size)))
                
    def create_tuman(self):
        self.tuman = pygame.Surface((100, 100))
        self.tuman.fill((0, 0, 0, 0))
        self.tuman.set_colorkey((0, 0, 0, 0))
        self.tumans = [pygame.image.load("1/tuman1_1.png")]
        self.betta_tuman = self.tumans[0]  
        self.mask_tuman = pygame.mask.from_surface(self.betta_tuman) 
        color_key = self.betta_tuman.get_at((0, 0))
        self.betta_tuman.set_colorkey(color_key)
        self.tuman.blit(self.betta_tuman, (0, 0))
        self.alpha_kanal = 255

    def update(self):
        if self.ch >= 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.img = self.frames[self.cur_frame]     
            self.image = pygame.transform.rotate(self.img, self.degrees_rotare)
            if self.ch < self.stop_time:
                self.become_tuman = Missiles.masshtab
                self.rect.x += self.vx 
                self.rect.y += self.vy
                self.ch += 1
            else:
                self.ch = -1
                self.coord_c = [*self.rect.center]
                self.become_tuman = Missiles.masshtab / 100
        elif self.ch == -1:
            self.img = self.tuman
            self.image = self.tuman
            self.mask = self.mask_tuman
            pep8 = 0 if osn_play.peremeshenie_fon == 0 else osn_play.speed
            self.coord_c[1] += pep8
            self.rect = self.img.get_rect(center=self.coord_c)
            if Missiles.masshtab + 50 >= self.become_tuman:
                self.become_tuman += Missiles.masshtab/100
                if int(self.become_tuman) < 1:
                    self.become_tuman = 1
                self.image = pygame.transform.scale(self.img,
                                                    (int(self.become_tuman),
                                                     int(self.become_tuman)))
                self.rect = self.image.get_rect(center=self.coord_c)
            else:
                self.image = self.img
                self.ch = -2
        else:
            if self.alpha_kanal <= 0:
                self.kill()
            self.tuman.set_alpha(self.alpha_kanal)
            self.tuman.set_colorkey((0, 0, 0))
            self.alpha_kanal -= 1
            self.mask = self.mask_tuman
            self.image = self.img
        
        self.rect.top += 0 if osn_play.peremeshenie_fon == 0 else osn_play.speed
        self.y0_fon = abs(osn_play.start_fon_position_for_y)
        if pygame.sprite.spritecollideany(self, sputnics):
            for i in range(len(sputnics.sprites())):
                try:
                    if pygame.sprite.collide_mask(self,sputnics.sprites()[i]):
                        self.vy = -self.vy 
                        if self.ch >= 0:
                            particle_count = 15
                            numbers = range(-5, 6)
                            for _ in range(particle_count):
                                Particle(sputnics.sprites()[i].rect.center,
                                         0, 0, sputnics.sprites()[i].radius,
                                         sputnics.sprites()[i].alpha,
                                         sputnics.sprites()[i].right)
                            sputnics.sprites()[i].kill()
                        else:
                            pep8_mat = 10 / (256 - self.alpha_kanal)
                            sputnics.sprites()[i].radius_down += pep8_mat
                except Exception:
                    print('error sputnics')
                    
        if pygame.sprite.spritecollideany(self, Missiles.group_parts):
            for i in range(len(Missiles.group_parts.sprites())):
                try:
                    pep8_group = Missiles.group_parts.sprites()[i]
                    if pygame.sprite.collide_mask(self, pep8_group):
                        local_ch = 1
                        self.vy = -self.vy 
                        if self.ch >= 0:
                            Missiles.group_parts.sprites()[i].kill()
                            Missiles.sound1.play()
                        else:
                            pep8_group = Missiles.group_parts.sprites()[i]
                            pep8_mat = 10 / (256 - self.alpha_kanal)
                            pep8_group.radius_down += pep8_mat
                except Exception:
                    print('error parts')
                        
    def redach_mashtab(self, value):
        Missiles.value -= value
        Missiles.masshtab -= (value*100)/750
        
    def create_group_parts(self, group):
        Missiles.group_parts = group
        Missiles.sound1 = pygame.mixer.Sound('1/boom.wav')


class Sputnics(pygame.sprite.Sprite):
    masshtab = 50
    osn_object = '-'
    group_parts = '-'

    def __init__(self, group):
        self.mass_sprites = [pygame.image.load("1/sputnic3_1.png"),
                             pygame.image.load("1/sputnic2.png"),
                             pygame.image.load("1/sputnic1.png")]
        super().__init__(group)
        self.img = choice(self.mass_sprites)
        self.mask = pygame.mask.from_surface(self.img)
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.alpha = choice(range(-30, 30,))/10
        self.radius = 800 + randrange(700)
        self.right = choice([-1,1])
        self.radius_down = 0
        self.masshtab = 0
        self.width,self.height = self.rect.size
        
    def update(self):
        self.alpha += 0.02 * self.right
        x = ((self.radius) * cos(self.alpha) + 500 - 66)
        pep8_mat = + Missiles.osn_object.start_fon_position_for_y + 420  - 44
        y = ((self.radius) * sin(self.alpha) + 1400 + pep8_mat)
        self.image = pygame.transform.scale(self.img,
                                            (int(Missiles.masshtab),
                                             int(Missiles.masshtab)))
        self.image1 = pygame.transform.rotate(self.image,
                                              -degrees(self.alpha) * self.right)
        self.mask = pygame.mask.from_surface(self.image1)
        self.rect = self.image1.get_rect()
        self.rect.center = x, y + (0 if sin(self.alpha) < 0 else 2000)
        '''
        if sin(self.alpha) > 0:
            self.rect.center = x, y
        else:
            self.rect.center = x, y + 2000
        '''
        if self.radius < 830:
            self.radius_down += 1
        if self.radius < 300:
            self.kill()
            Missiles.osn_object.coins += 100
        if self.radius_down != 0:
            if self.radius_down > 170:
                particle_count = 15
                numbers = range(-5, 6)
                for _ in range(particle_count):
                    Particle(self.rect.center, x, y, self.radius, self.alpha,
                             self.right)
                pep8_group = Missiles.group_parts.sprites()[0]
                pep8_group.osn_object_function(Missiles.osn_object)
                self.kill()
            self.radius -= self.radius_down/10
            self.radius_down -= self.radius_down/10            
       
    def redach_mashtab(self, value):
        Missiles.masshtab -= (value*100)/750    
       
    def osn_object_function(self, obj):
        Missiles.osn_object = obj
        
    def create_group_parts(self, group):
        Missiles.group_parts = group
 
        
class Radar():
    def __init__(self):
        pass

     
class Music():
    def __init__(self):
        self.melodia = '-'
        self.volue = 1
        self.speed_volue = 0.05
        #print('init_music')
    def render(self):
        if why_screen[0] == 'menu' and self.melodia != 'menu':
            if self.volue > 0:
                self.volue -= self.speed_volue
                pygame.mixer.music.set_volume(self.volue)
            else:
                self.volue = 1
                pygame.mixer.music.set_volume(self.volue)              
                pygame.mixer.music.load('1/menu.wav')
                pygame.mixer.music.play(-1)
                self.melodia = 'menu'
        elif why_screen[0] == 'start_game' and self.melodia != 'start_game':
            if self.volue > 0:
                self.volue -= self.speed_volue
                pygame.mixer.music.set_volume(self.volue)
            else:
                self.volue = 1
                pygame.mixer.music.set_volume(self.volue)              
                pygame.mixer.music.load('1/start.wav')
                pygame.mixer.music.play(-1)
                self.melodia = 'start_game'      
        elif why_screen[0] == 'game' and self.melodia != 'game':
            if self.volue > 0:
                self.volue -= self.speed_volue
                pygame.mixer.music.set_volume(self.volue)
            else:
                self.volue = 1
                pygame.mixer.music.set_volume(self.volue)            
                pygame.mixer.music.load('1/game.wav')
                pygame.mixer.music.play(-1)
                self.melodia = 'game'      
        elif why_screen[0] == 'shop' and self.melodia != 'shop':
            if self.volue > 0:
                self.volue -= self.speed_volue
                pygame.mixer.music.set_volume(self.volue)
            else:
                self.volue = 1
                pygame.mixer.music.set_volume(self.volue)
                pygame.mixer.music.load('1/shop.wav')
                pygame.mixer.music.play(-1)
                self.melodia = 'shop'                 


class PlayClass():
    def __init__(self, max_h, time_max, extremums, extremums_sp, fps, coins,
                 sputnics, missiles, prticles, who_shar=1):
        self.start_fon_position_for_y = -1700
        self.very_max = 65482
        self.radius_shar = 31
        self.create_class(sputnics, missiles, prticles)
        self.create_init_tools(fps)
        self.delete_this_ch = 0
        self.download_convas()
        self.now_start(who_shar1=who_shar)
        self.restart(0, max_h, time_max, extremums, extremums_sp)
        self.tupe_pul = []
        self.coins = coins
        
    def now_start(self, who_shar1=1):
        self.create_shar(who_shar=who_shar1)
        self.create_fon()
        self.create_const()  
        
    def create_fon(self):
        self.peremeshenie_fon = 1
        self.fon_mashtab_step_for_start_x = 2000
        self.fon_mashtab_step_for_start_y = 2000
        self.start_fon_position_for_y = -1950
        self.start_fon_position_for_x = -500
        self.start_fon_position_for_player_y = -1850
        self.start_fon_position_for_player_x = -500
        self.for_player_step_x = -2
        self.start_fon_position_for_x_kostil = 0
        self.start_fon_position_for_y_kostil = 0
        
    def download_convas(self):
        self.fon = pygame.image.load("1/fon6.png").convert()
        self.fon_rect = pygame.Rect(-10, -10, 1020, 620)
        self.shar = pygame.image.load("1/shar1_2.png").convert_alpha()
        self.pul1_how = pygame.image.load("1/pul1_how.png").convert_alpha()
        self.coin_image = pygame.image.load("1/coin.png").convert_alpha()
        self.coin_image_rect = self.coin_image.get_rect(centery=75, left=10)
        self.surf = pygame.Surface((2000, 2500), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0, 0))
        
    def create_shar(self, who_shar=1): 
        self.who_shar = who_shar
        pep8_str = "1/shar"+str(self.who_shar)+"_2.png"
        self.shar = pygame.image.load(pep8_str).convert_alpha()        
        self.shar1 = self.shar.copy()
        self.shar1_rect = self.shar1.get_rect(centerx=500, bottom=470)
        self.shar1_rect_impuls = self.shar1_rect
        self.x, self.y = self.shar1_rect.topleft
        self.x_im, self.y_im = self.x, self.y
        self.shar_mashtab_step_for_start_x = 116
        self.shar_mashtab_step_for_start_y = 116 
        self.bufer_y = 0
        self.speed = 0
        self.how_many_pul = 0
        
        
    def create_class(self, sputnics, missiles, prticles):
        self.sputnics = sputnics
        self.missiles = missiles
        
        self.prticles = prticles
        Sputnics(self.sputnics)        
        Missiles(self.missiles, (-100, -100), (-201, -201), 1, 250)
        self.missiles.sprites()[0].create_osn_class(self)
        self.missiles.sprites()[0].create_group_parts(self.prticles)
        self.sputnics.sprites()[0].osn_object_function(self)
        
        
    def create_init_tools(self, fps):
        self.fps = fps
        
    def create_const(self):
        self.ch1 = 0
        self.ch2 = -1
        self.ch3 = -1
        self.m0 = 60
        self.pul_mas = 10
        self.m = self.m0
        self.key_down, self.key_up = False, False
        self.chetchic1 = 0
        self.now_time = time()
        self.speed_x, self.speed_y = 0, 0
        self.fast_rise = False
        
    def restart(self, ch, max_h, time_max, extremums, extremums_sp):
        self.how_many_pul = ch
        self.m = self.m0 + self.pul_mas*ch        
        self.extremums = extremums
        self.extremums_sp = extremums_sp
        self.max_h_fiying = max_h
        self.time_max_fliting = time_max  
        try:
            max_h_fiying = max(self.extremums, key=lambda i: i[1])
            #print(max_h_fiying)
            self.max_h_fiying_index = self.extremums.index(max_h_fiying)
            self.time_max_fliting, self.max_h_fiying = max_h_fiying
        except Exception as e:
            print(e)
        for i in self.missiles.sprites()[::-1]:
            i.kill()
        
    def key_button_control(self):
        if self.key_up:
            self.y -= 10
        if self.key_down:
            self.y += 10

    def set_view(self, left, top, cell_size):
        pass
        
    def get_click(self, mouse_pos):
        try:
            cell = self.get_cell(mouse_pos)
            self.on_click(self, cell)
        except Exception as e:
            pass

    def get_cell(self, cort):
        x, y = pygame.mouse.get_pos()
        return x, y
    
    def on_click(self, rr, cell):
        if self.how_many_pul > 0:
            Missiles(self.missiles,
                     (self.shar1_rect_impuls.center), cell,
                     self.tupe_pul[0][0], Smax=self.tupe_pul.pop(0)[1])
            self.m -= self.pul_mas
            self.impuls_speed(self.missiles.sprites()[-1])
            self.how_many_pul -= 1
            
    def plus(self):
        if self.peremeshenie_fon != 1:
            self.start_fon_position_for_x_kostil = -10
            self.start_fon_position_for_y_kostil = -10
            self.fon_mashtab_step_for_start_x += 20
            self.fon_mashtab_step_for_start_y += 20   
            self.shar_mashtab_step_for_start_x += 1.16
            self.shar_mashtab_step_for_start_y += 1.16
        
    def minus(self):
        if self.peremeshenie_fon != 1:
            self.start_fon_position_for_x_kostil = 10
            self.start_fon_position_for_y_kostil = 10
            self.fon_mashtab_step_for_start_x -= 20
            self.fon_mashtab_step_for_start_y -= 20 
            self.shar_mashtab_step_for_start_x -= 1.16
            self.shar_mashtab_step_for_start_y -= 1.16   
            
    def speed_raschet(self, m_time):
        self.delete_this_ch += 1
        pep8_mat = self.start_fon_position_for_y - self.shar1_rect.top
        if self.peremeshenie_fon == 3 and pep8_mat < -2170:
            self.speed = 0
            why_screen[0] = "start_game"
            shop_screen.repit_function()
        try:
            pep8_mat =  (self.extremums[(self.ch3 if self.ch3 >= 0 else 0)][1])
            pep8_log = pep8_mat > self.max_h_fiying - 1500
            if self.fast_rise or (self.peremeshenie_fon == 1 and  pep8_log):
                self.peremeshenie_fon = 0
                if self.fast_rise:
                    self.ch2 = self.max_h_fiying_index - 1
        except Exception as e:
            print(e)
        if self.peremeshenie_fon != 3:
            try:
                time_ex, h = self.extremums[self.ch2+1]
                if m_time  >= time_ex or self.fast_rise:
                    if self.fast_rise:
                        self.fast_rise = False
                        pep8 = self.speed * (time_ex - m_time) * 30
                        self.start_fon_position_for_y += pep8
                    self.ch2 += 1
                    self.ch3 += 1
                
                    new_t, new_h = self.extremums[self.ch2+1]
                    if m_time == 0:
                        m_time = time() - self.now_time
                    pep8 = ((new_h - h) / (new_t - m_time))
                    self.speed = pep8 / (self.fps * 20)
            except Exception as e:
                print(e)
        else:
            self.speed = -1.7

    def impuls_speed(self, pul):
        self.speed_x -= (self.pul_mas * pul.vx) / self.m
        self.speed_y -= (self.pul_mas * pul.vy) / self.m

    def speeds_control(self): 
        k = -0.01
        if abs(self.speed_x) - k < 0:
            self.speed_x = 0
        if abs(self.speed_y) - k < 0:
            self.speed_y = 0
        if self.speed_x != 0:
            if self.speed_x > 0:
                self.speed_x += k
            elif self.speed_x < 0:
                self.speed_x -= k
        if self.speed_y != 0:
            if self.speed_y>0:
                self.speed_y += k
            elif self.speed_y < 0:
                self.speed_y -=k  
        if round(self.y_im) != round(self.y):
            self.speed_y += (self.y - self.y_im) / 10
        
    def render(self):
        if True:
            self.fon_copy = self.fon
            m_time = int((time() - self.now_time))
            try:
                self.speed_raschet(m_time*2)
            except Exception as e:
                print(e)
            if m_time <= 200:
                if self.peremeshenie_fon in [1, 2, 3]:
                    self.start_fon_position_for_y += self.speed
                if self.peremeshenie_fon == 0:
                    self.y -= self.speed

            self.key_button_control()
            self.surf = self.fon
            self.shar1 = self.shar
            if self.chetchic1 >= 490 and self.peremeshenie_fon == 1:
                self.peremeshenie_fon = 0
            if self.start_fon_position_for_x_kostil != 0:
                pep8 = self.start_fon_position_for_x_kostil
                self.start_fon_position_for_x += pep8
                pep8 = self.start_fon_position_for_y_kostil
                self.start_fon_position_for_y += pep8
                try:
                    pep8 = self.start_fon_position_for_x_kostil
                    self.sputnics.sprites()[0].redach_mashtab(pep8)
                    pep8 = self.start_fon_position_for_x_kostil
                    self.missiles.sprites()[0].redach_mashtab(pep8)
                except Exception:
                    pass
            self.bufer_y = self.speed
            
            screen.blit(self.surf, (self.start_fon_position_for_x,
                                    self.start_fon_position_for_y))
            self.start_fon_position_for_x_kostil = 0
            self.start_fon_position_for_y_kostil = 0
            self.x_im += self.speed_x
            self.y_im += self.speed_y
            self.speeds_control()
            self.shar1_rect.topleft = self.x_im, self.y
            self.shar1_rect_impuls.topleft = self.x_im, self.y_im
            if self.speed_y == 0:
                screen.blit(self.shar1, self.shar1_rect)
            else: 
                screen.blit(self.shar1, self.shar1_rect_impuls)           
            self.sputnics.draw(screen)
            self.sputnics.update()    
            self.prticles.draw(screen)
            self.prticles.update() 
            self.missiles.draw(screen)
            self.missiles.update()  
            font = pygame.font.Font(None, 34)
            text = font.render(str(self.how_many_pul), 1, (100, 100, 255))
            text_rect = text.get_rect(centery=40, left=50)
            pul1_how_tect = self.pul1_how.get_rect(centery=40, left=10)
            coins_text = font.render(str(self.coins), 1, (100, 100, 255))
            coins_text_rect = coins_text.get_rect(centery=75, left=50)
            screen.blit(self.pul1_how, pul1_how_tect) 
            screen.blit(self.coin_image, self.coin_image_rect)
            screen.blit(text, text_rect)
            screen.blit(coins_text, coins_text_rect)
            print(len(self.sputnics.sprites()))
            if not(self.fon_rect.colliderect(self.shar1_rect)):
                why_screen[0] = "game_over"
            if len(self.sputnics.sprites()) < 5:
                for i in range(choice(range(1, 4))):
                    Sputnics(sputnics)                
                a = sum([1 for i in self.sputnics.sprites() if i.radius > 970])
                self.sputnics.sprites()[-1].radius = 800 + choice(range(1, 100))
                print('------------------------------------------------')
        self.ch1 += 1
        

class Button():
    def __init__(self, image, cell, what_return):
        self.image_button = image
        self.rect_button = self.image_button.get_rect(center=cell)
        self.what_return = what_return

    def render(self, cell, otvet_no):
        screen.blit(self.image_button, self.rect_button)
        if self.rect_button.collidepoint(cell):
            return self.what_return
        else:
            return otvet_no

class LearnClass():
    def __init__(self):
        self.fon = pygame.image.load("1/learn2.png").convert()
        pep8_str = "1/menu_button2.png"
        self.menu_button_img = pygame.image.load(pep8_str).convert_alpha()
        self.menu_button = Button(self.menu_button_img,(500,550),"menu")
        self.mouse = (-1, -1)
        
    def repit(self):
        self.mouse = (-1, -1)
        self.menu_button = Button(self.menu_button_img,(500,550),"menu")
        
    def render(self):
        screen.blit(self.fon, (0, 0))
        a = self.menu_button.render(self.mouse, why_screen[0])
        if a != 'learn':
            screen_menu.repit()  
        why_screen[0] = a
        
class Menu():
    def __init__(self):
        self.fon = pygame.image.load("1/menu_fon2.jpg").convert()
        open_img = "1/start_button2.png"
        self.start_button_img = pygame.image.load(open_img).convert_alpha()
        self.start_button = Button(self.start_button_img,(500,300),"start_game")
        self.shop = pygame.image.load("1/shop_button3.png").convert_alpha()
        self.lern = pygame.image.load("1/learning_button.png").convert_alpha()
        self.shop_button = Button(self.shop,(500,375),"shop")
        self.learn_button = Button(self.lern,(500,225),"learn")
        self.mouse = (-1, -1)

    def repit(self):
        self.shop_button = Button(self.shop,(500,375),"shop")
        self.start_button = Button(self.start_button_img,(500,300),"start_game")
        self.learn_button = Button(self.lern,(500,225),"learn")
        self.mouse = (-1, -1)

    def render(self):
        screen.blit(self.fon, (0, 0))
        a = self.shop_button.render(self.mouse, why_screen[0])
        if a != 'menu':
            shop_shar.repit()  
        why_screen[0] = a
        a = self.start_button.render(self.mouse, why_screen[0])
        if a != 'menu':
            shop_screen.repit_function()
        why_screen[0] = a 
        a = self.learn_button.render(self.mouse, why_screen[0])
        if a != 'menu':
            learn_class.repit()
        why_screen[0] = a                


class Board:
    def __init__(self, width, height, x, y, tupe, coins, m=10, Smax=250):
        self.width = width
        self.height = height
        self.x, self.y = x, y
        self.tupe = tupe
        self.prise = coins
        self.m = m
        self.Smax = Smax
        x, y = 0, 0
        self.pul = pygame.image.load("1/pul1_1x1.png").convert_alpha()
        self.yach = pygame.image.load("1/one_yacheyka.png").convert()
        rect = self.yach.get_rect()
        self.board = [[self.yach.get_rect(topleft=(j*rect.width + self.x,
                                                    i*rect.height + self.y))
                        for i in range(height)][::] for j in range(width)]
        self.board_bul = [[[None, (j*rect.width + self.x,
                                   i*rect.height + self.y),
                            tupe, coins, self.m, self.Smax].copy()
                           for i in range(height)][::] for j in range(width)]
        self.board_rect = pygame.Rect(self.x, self.y,
                                      self.width*rect.width,
                                      self.height*rect.height)
        self.left = 110
        self.top = 110
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        
    def get_click(self, mouse_pos):
        string = "<class 'pygame.Rect'>"
        if self.board_rect.collidepoint(mouse_pos): 
            for i in range(len(self.board_bul)):
                for j in range(len(self.board_bul[i])):
                    if str(type(self.board_bul[i][j][1])) == string:
                        if self.board_bul[i][j][1].collidepoint(mouse_pos):
                            cell = self.get_cell(mouse_pos)
                            self.on_click(self, cell)
                            return (i, j, self.board_bul[i][j][0],
                                    self.board_bul[i][j][1])
        return None
        
    def get_cell(self, cort):
        x, y = pygame.mouse.get_pos()
        x, y = (x - self.left)//self.cell_size, (y - self.top)//self.cell_size
        if x >= 0 and x <= self.width and y >= 0 and y <= self.height:
            return (x, y,)
    
    def on_click(self, obg, cell):
        if cell:
            pass

    def render(self):
        string = "<class 'pygame.Rect'>"
        for i in range(self.width):
            for j in range(self.height):
                screen.blit(self.yach , self.board[i][j])
                if str(type(self.board_bul[i][j][1])) == string:
                    screen.blit(*self.board_bul[i][j][:2:])
                    

class MissileShop():
    def __init__(self, osnov_class, mo, extremums, who_shar=1):
        self.mas_pul = 0
        self.osnov_class = osnov_class
        self.mo = mo
        self.maxh = 65
        self.r = 31
        self.who_shar = who_shar
        self.coin_image = pygame.image.load("1/coin.png").convert_alpha()
        self.coin_rect1 = self.coin_image.get_rect(bottom=330, centerx=475)
        self.coin_rect2 = self.coin_image.get_rect(bottom=330, centerx=525)
        self.coin_rect3 = self.coin_image.get_rect(centery=45, left=10)
        self.fon = pygame.image.load("1/fon6.png").convert()
        open_img = "1/start_button2.png"
        self.start_button_img = pygame.image.load(open_img).convert_alpha()
        open_img = "1/menu_button2.png"
        self.menu_button_img = pygame.image.load(open_img).convert_alpha()
        open_img = "1/shar" + str(self.who_shar) + "_2.png"
        self.shar = pygame.image.load(open_img).convert_alpha()
        self.shar_rect = self.shar.get_rect(left=470, bottom=why_screen[2])
        self.texr_fon = pygame.image.load("1/text3.png").convert_alpha()
        self.start_button = Button(self.start_button_img, (700, 450), "game")
        self.menu_button = Button(self.menu_button_img, (700, 530), "menu")
        self.extremums = extremums
        self.board_bag = Board(4, 5, 100, 50, -1, 0)
        self.board_shop = Board(1, 5, 400, 50, 1, 0)
        self.board_shop2 = Board(1, 5, 450, 50, 2, 10, Smax=400)
        self.board_shop3 = Board(1, 5, 500, 50, 3, 15, m=5)
        self.pul = pygame.image.load("1/pul1_1x1.png").convert_alpha()
        self.pul5 = pygame.image.load("1/pul1_1x5.png").convert_alpha()
        self.pul10 = pygame.image.load("1/pul1_1x10.png").convert_alpha()
        self.pul20 = pygame.image.load("1/pul1_1x20.png").convert_alpha()
        self.pulall = pygame.image.load("1/pul1_1xall.png").convert_alpha()
        self.pul_2 = pygame.image.load("1/pul2_1x1.png").convert_alpha()
        self.pul5_2 = pygame.image.load("1/pul2_1x5.png").convert_alpha()
        self.pul10_2 = pygame.image.load("1/pul2_1x10.png").convert_alpha()
        self.pul20_2 = pygame.image.load("1/pul2_1x20.png").convert_alpha()
        self.pulall_2 = pygame.image.load("1/pul2_1xall.png").convert_alpha()
        self.pul_3 = pygame.image.load("1/pul3_1.png").convert_alpha()
        self.pul5_3 = pygame.image.load("1/pul3_1x5.png").convert_alpha()
        self.pul10_3 = pygame.image.load("1/pul3_1x10.png").convert_alpha()
        self.pul20_3 = pygame.image.load("1/pul3_1x20.png").convert_alpha()
        self.pulall_3 = pygame.image.load("1/pul3_1xall.png").convert_alpha() 
        self.font1 = pygame.font.Font(None, 34)
        self.font2 = pygame.font.Font(None, 20)
        self.font3 = pygame.font.Font(None, 20)
        self.font4 = pygame.font.Font(None, 50)
        self.bag = self.font1.render('Берём с собой:', 1, (255, 255, 255))
        self.shop = self.font1.render('Магазин', 1, (255, 255, 255)) 
        self.price1 = self.font2.render(str(10), 1, (0, 0, 255))
        self.price2 = self.font2.render(str(15), 1, (0, 0, 255))
        self.logining_text = self.font4.render('Генерация полёта...',
                                               1, (255, 255, 255))
        self.m_shar = self.font3.render("Масса шара " + str(self.mo), 1,
                              (255, 255, 255))
        text = "Max высота без груза " + str(self.maxh) + 'т.'
        self.fly = self.font3.render(text, 1, (255, 255, 255))
        self.m = self.font3.render('Mасса ' + str(self.mo + self.mas_pul), 
                         1, (255, 255, 255))
        self.radius = self.font3.render('Радиус шара ' + str(self.r), 1,
                                   (255, 255, 255))        
        self.price1_rect = self.price1.get_rect(center=self.coin_rect1.center)
        self.price2_rect = self.price2.get_rect(center=self.coin_rect2.center) 
        self.logining_text_rect = self.logining_text.get_rect(center=(500,300))
        self.down_button = False
        self.loading = False
        self.mouse_coord = -1, -1
        self.mouse_img, self.mouse_img_rect = None, None
        self.ch = 0
        self.tupe_pul = -1
        self.surf_black1 = pygame.Surface((1000,600), pygame.SRCALPHA)
        self.surf_black1.fill((0, 0, 0, 150))        
        top_l_list = [self.board_shop.board_bul[0][0][1],
                      self.board_shop.board_bul[0][1][1],
                      self.board_shop.board_bul[0][2][1],
                      self.board_shop.board_bul[0][3][1],
                      self.board_shop.board_bul[0][4][1],
                      
                      self.board_shop2.board_bul[0][0][1],
                      self.board_shop2.board_bul[0][1][1],
                      self.board_shop2.board_bul[0][2][1],
                      self.board_shop2.board_bul[0][3][1],
                      self.board_shop2.board_bul[0][4][1],
                      
                      self.board_shop3.board_bul[0][0][1],
                      self.board_shop3.board_bul[0][1][1],
                      self.board_shop3.board_bul[0][2][1],
                      self.board_shop3.board_bul[0][3][1],
                      self.board_shop3.board_bul[0][4][1]]
        
        rect_list = [self.pulall.get_rect(topleft=top_l_list[0]),
                     self.pul20.get_rect(topleft=top_l_list[1]),
                     self.pul10.get_rect(topleft=top_l_list[2]),
                     self.pul5.get_rect(topleft=top_l_list[3]),
                     self.pul.get_rect(topleft=top_l_list[4]),
                     
                     self.pulall_2.get_rect(topleft=top_l_list[5]),
                     self.pul20_2.get_rect(topleft=top_l_list[6]),
                     self.pul10_2.get_rect(topleft=top_l_list[7]),
                     self.pul5_2.get_rect(topleft=top_l_list[8]),
                     self.pul_2.get_rect(topleft=top_l_list[9]),
                     
                     self.pulall_3.get_rect(topleft=top_l_list[10]),
                     self.pul20_3.get_rect(topleft=top_l_list[11]),
                     self.pul10_3.get_rect(topleft=top_l_list[12]),
                     self.pul5_3.get_rect(topleft=top_l_list[13]),
                     self.pul_3.get_rect(topleft=top_l_list[14])]
        
        self.board_shop.board_bul[0][0][:2:] = [self.pulall, rect_list[0]]
        self.board_shop.board_bul[0][1][:2:] = [self.pul20, rect_list[1]]
        self.board_shop.board_bul[0][2][:2:] = [self.pul10, rect_list[2]]
        self.board_shop.board_bul[0][3][:2:] = [self.pul5, rect_list[3]]
        self.board_shop.board_bul[0][4][:2:] = [self.pul, rect_list[4]]
        
        self.board_shop2.board_bul[0][0][:2:] = [self.pulall_2, rect_list[5]]
        self.board_shop2.board_bul[0][1][:2:] = [self.pul20_2, rect_list[6]]
        self.board_shop2.board_bul[0][2][:2:] = [self.pul10_2, rect_list[7]]
        self.board_shop2.board_bul[0][3][:2:] = [self.pul5_2, rect_list[8]]
        self.board_shop2.board_bul[0][4][:2:] = [self.pul_2, rect_list[9]]
        
        self.board_shop3.board_bul[0][0][:2:] = [self.pulall_3, rect_list[10]] 
        self.board_shop3.board_bul[0][1][:2:] = [self.pul20_3, rect_list[11]]
        self.board_shop3.board_bul[0][2][:2:] = [self.pul10_3, rect_list[12]]
        self.board_shop3.board_bul[0][3][:2:] = [self.pul5_3, rect_list[13]] 
        self.board_shop3.board_bul[0][4][:2:] = [self.pul_3, rect_list[14]]    
        
    def get_click(self, mouse_pos):
        a = None
        if self.board_shop.board_rect.collidepoint(mouse_pos):
            a = self.board_shop.get_click(mouse_pos)
            self.tupe_pul = 1
        elif self.board_shop2.board_rect.collidepoint(mouse_pos):
            self.tupe_pul = 2
            a = self.board_shop2.get_click(mouse_pos)  
        elif self.board_shop3.board_rect.collidepoint(mouse_pos):
            self.tupe_pul = 3
            a = self.board_shop3.get_click(mouse_pos)    
        elif self.board_bag.board_rect.collidepoint(mouse_pos):
            pass
        if a:
            x, y, self.mouse_img, self.mouse_img_rect = a
            if y == 0:
                self.ch = 100
            elif y == 1:
                self.ch = 20
            elif y == 2:
                self.ch = 10  
            elif y == 3:
                self.ch = 5      
            else:
                self.ch = 1  
        self.mouse_coord = mouse_pos

    def get_cell(self, cort):
        x, y = pygame.mouse.get_pos()
        x = (x - self.left) // self.cell_size
        y = (y - self.top) // self.cell_size
        if x >= 0 and x <= self.width and y >= 0 and y <= self.height:
            return (x, y,)
    
    def on_click(self, obg, cell):
        if cell:
            pass

    def repit_function(self):
        self.loading = False
        self.start_button = Button(self.start_button_img, (700, 450), "game")
        self.menu_button = Button(self.menu_button_img, (700, 530), "menu")
        self.down_button = False
        self.mouse_coord = -1, -1
        self.mouse_img, self.mouse_img_rect = None, None
        self.mas_pul = 0
        self.ch = 0     
        self.board_bag = Board(4, 5, 100, 50, -1, 0)
        open_img = "1/shar" + str(self.who_shar) + "_2.png"
        self.shar = pygame.image.load(open_img).convert_alpha()
        self.shar_rect = self.shar.get_rect(left=470, bottom=why_screen[2])
        self.m_shar = self.font3.render("Масса шара " + str(self.mo), 1,
                              (255, 255, 255))
        text = "Max высота без груза " + str(self.maxh) + 'т.'
        self.fly = self.font3.render(text, 1, (255, 255, 255))
        self.m = self.font3.render('Mасса ' + str(self.mo + self.mas_pul), 
                         1, (255, 255, 255))
        self.radius = self.font3.render('Радиус шара ' + str(self.r), 1,
                                   (255, 255, 255))        
    def start_game_screen(self):       
        ch = 0
        self.osnov_class.tupe_pul = []
        local_herf = self.osnov_class.tupe_pul
        local_m = []
        for i in range(len(self.board_bag.board_bul)):
            for j in range(len(self.board_bag.board_bul[i])): 
                if self.board_bag.board_bul[i][j][0]:
                    local_herf.append([self.board_bag.board_bul[i][j][2],
                                       self.board_bag.board_bul[i][j][5]])
                    local_m.append(self.board_bag.board_bul[i][j][4])
                    ch += 1
        self.osnov_class.tupe_pul = local_herf 
        mo = int(self.mo + sum(local_m))
        #print('=====', self.osnov_class.tupe_pul)
        try:
            self.loading = False
            print("try")
            string = 'mass_' + str(mo) + '_' + str(self.r)
            masss = importlib.import_module(string)
        except Exception:
            screen.blit(self.surf_black1, (0, 0))
            screen.blit(self.logining_text, self.logining_text_rect) 
            pygame.display.flip()                         
            self.loading = True
            print('ex')
            #local_rect = pygame.Rect(0,0,1000,600)
            import make_massivs
            make_massivs.func(mo, self.r)
            f = open('mass_' + str(mo) + '_' + str(self.r) + '.py', 'r')
            f.close()
            strind = 'mass_' + str(mo)+ '_' + str(self.r)
            masss = importlib.import_module(strind)
        masss = importlib.import_module('mass_' + str(mo)+ '_' + str(self.r))
        print(mo)
        print(self.r)
        self.extremums = masss.mass[::]
        self.extremums_sp = masss.mass_sp[::]
        self.osnov_class.tupe_pul.sort(reverse=True, key=lambda i: i[0])
        self.osnov_class.now_start(who_shar1=self.who_shar)
        self.osnov_class.restart(ch, masss.max_h,
                                 masss.time_max, self.extremums,
                                 self.extremums_sp)
        
    def render(self):
        screen.blit(self.fon, (-500, why_screen[1]))
        screen.blit(self.shar, self.shar_rect)
        self.board_bag.render()
        self.board_shop.render()
        self.board_shop2.render()
        self.board_shop3.render()
        coins_text = self.font1.render(str(self.osnov_class.coins), 1,
                                       (100, 100, 255))
        coins_text_rect = coins_text.get_rect(centery=45, left=50)
        screen.blit(self.coin_image, self.coin_rect1)
        screen.blit(self.coin_image, self.coin_rect2)
        screen.blit(self.coin_image, self.coin_rect3)
        screen.blit(coins_text, coins_text_rect)  
        screen.blit(self.price1, self.price1_rect)
        screen.blit(self.price2, self.price2_rect)
        screen.blit(self.texr_fon, (200,390))
        screen.blit(self.m_shar, (240, 440))
        screen.blit(self.fly, (240, 460))
        screen.blit(self.m, (240, 480))
        screen.blit(self.radius, (240, 500))
        screen.blit(self.bag, (100, 20))
        screen.blit(self.shop, (430, 20))
        if self.loading:
            print("===================================")
            screen.fill((0, 0, 0, 150))
            screen.blit(self.logining_text, self.logining_text_rect) 
            pygame.display.flip()
        #screen.fill((0, 0, 0, 150))
        #screen.blit(self.logining_text, self.logining_text_rect)               
        if str(self.down_button) == '1':
            self.down_button = False
            if self.board_bag.board_rect.collidepoint(self.mouse_coord):
                for i in range(len(self.board_bag.board_bul)):
                    for j in range(len(self.board_bag.board_bul[i])): 
                        if not(self.board_bag.board_bul[i][j][0]):
                            try:
                                if self.tupe_pul == 1:
                                    local_img = self.pul
                                    local_prise = 0
                                    class_shop = self.board_shop
                                    
                                elif self.tupe_pul == 2:
                                    local_prise = 10
                                    local_img = self.pul_2
                                    class_shop = self.board_shop2
                                elif self.tupe_pul == 3:
                                    local_prise = 15
                                    local_img = self.pul_3      
                                    class_shop = self.board_shop3
                                if self.osnov_class.coins - local_prise < 0:
                                    break
                                self.osnov_class.coins -= local_prise
                                coord = self.board_bag.board_bul[i][j][1][::]
                                loc_herf = class_shop.board_bul[0][4][::]
                                self.board_bag.board_bul[i][j] = loc_herf
                                pep8 = self.pul.get_rect(topleft = coord)
                                self.board_bag.board_bul[i][j][1] = pep8
                                self.mas_pul += class_shop.m
                                self.ch -= 1
                            except Exception as e:
                                print('erorr pul_render', e)
                        if self.ch <=0 or self.osnov_class.coins < 0:
                            break
                    if self.ch <=0 or self.osnov_class.coins < 0:
                        break
        
        elif not(self.down_button):
            self.mouse_img = None 
        if self.mouse_img:
            screen.blit(self.mouse_img, self.mouse_coord)
        
        a = self.start_button.render(self.mouse_coord, why_screen[0])      
        if a == "game":
            self.start_game_screen()
        why_screen[0] = a
        a = self.menu_button.render(self.mouse_coord, why_screen[0])
        if a == "menu":
            screen_menu.repit()
        why_screen[0] = a


def print_text(string,topleft1,font=None, font_size=10,return_surf=False):
    surf = pygame.Surface((200, 200), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))
    if font:
        pass
    else:
        font = pygame.font.Font(None, font_size)
    str_list = string.split('\n')
    post_text_rect = pygame.Rect(-1,30,1,1)
    for i in str_list:  
        text = font.render(i, 1, (255, 255, 255))
        text_rect = text.get_rect(top=post_text_rect.bottom,
                                  left=post_text_rect.left)
        if return_surf:
            pass
        else:
            surf.blit(text, text_rect)
            post_text_rect = text_rect.copy()
    return surf


class Product():
    nomber = 1
    nomber1 = 1

    def __init__(self, img, topleft1, text, font1, num, prise, m0, r, h,
                 open1=False):
        self.ok_change = [pygame.image.load("1/ok.png").convert_alpha()]    
        self.img = img
        self.num = num
        self.open1 = open1
        self.prise = prise
        self.m0 = m0
        self.r = r
        self.maxh = h
        if self.open1:
            self.prise = 0
        self.rect = self.img.get_rect(topleft=topleft1)
        self.text = print_text(text, self.rect.topleft, font=font1)
        self.text_rect = self.text.get_rect(topleft=(self.rect.left,
                                                     self.rect.bottom))
        self.surf_black1 = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.surf_black1.fill((0, 0, 0, 150))       
        pep8 = self.ok_change[0].get_rect(center=self.rect.center)
        self.ok_change_rect = pep8
        
    def render(self, render_qestion):
        screen.blit(self.img, self.rect)
        screen.blit(self.text, self.text_rect)
        if not(self.open1):
            screen.blit(self.surf_black1, self.rect )
        else:
            pass
        if Product.nomber == self.num:
            if self.open1:
                screen.blit(self.ok_change[0], self.ok_change_rect)
                Product.nomber1 = self.num
            else:
                return True
        return render_qestion
    
    def add_nomber(self, num):
        Product.nomber = num
        
    def give_nomber(self):
        return Product.nomber
    
    def add_nomber1(self, num):
        Product.nomber1 = num
        
    def give_nomber1(self):
        return Product.nomber1    
    
    
class Question():
    def __init__(self, mass, shars, shop_class,
                 osn_play, shar1_class):
        self.font4 = pygame.font.Font(None, 50)
        self.logining_text = self.font4.render('Динамика полёта...',
                                               1, (255, 255, 255))
        self.logining_text_rect = self.logining_text.get_rect(center=(500,300))
        self.surf_black2 = pygame.Surface((1000, 600), pygame.SRCALPHA)
        self.surf_black2.fill((0, 0, 0, 150))         
        self.osn_play = osn_play
        self.opens = mass
        self.shars = shars
        self.shop_class = shop_class
        self.fon = pygame.image.load("1/qu.png")
        self.fon_rect = self.fon.get_rect()
        self.answer_qu = ['see']
        self.clik_class = shar1_class 
        self.no_button = Button(pygame.image.load("1/qu_no.png"),
                                (self.fon_rect.left + 90,
                                 self.fon_rect.top + 138),  'close')
        self.yes_button = Button(pygame.image.load("1/qu_yes.png"),
                                 (self.fon_rect.left + 210,
                                  self.fon_rect.top + 138),  'yes')

    def render(self, mouse):
        screen.blit(self.fon, (0, 0))
        a = self.no_button.render(mouse, self.answer_qu[0])
        if a == 'close':
            self.shop_class.render_qestion = False
            a = 'see'
        self.answer_qu[0] = a
        if self.osn_play.coins >= self.clik_class.prise:
            a = self.yes_button.render(mouse, self.answer_qu[0])
            if a == 'yes':
                self.shop_class.render_qestion = False
                self.clik_class.open1 = True
                self.osn_play.coins -= self.clik_class.prise
                f = self.clik_class.give_nomber() - 2
                if f >= 0:
                    self.opens[f] = True
                self.clik_class.prise = 0
                self.shars[0] = self.clik_class.give_nomber()
                if self.opens[0]:
                    self.shars[1] += '$'
                if self.opens[1]:
                    self.shars[1] += '%'
                if self.opens[2]:
                    self.shars[1] += '^' 
                a = 'see'
                screen.blit(self.surf_black2, (0, 0))
                screen.blit(self.logining_text, self.logining_text_rect)  
                pygame.display.flip()
                import make_massivs
                make_massivs.func(self.clik_class.m0, self.clik_class.r,
                                  graph=True)
                self.clik_class
            self.answer_qu[0] = a


class ShopShar():
    def __init__(self, shars, osn_play, shop_screen):
        self.shop_screen = shop_screen
        self.osn_play = osn_play
        self.shars = shars
        self.opens = [False, False, False]
        self.fon = pygame.image.load("1/fon_shop3.png").convert()
        self.font3 = pygame.font.Font(None, 20)
        if '$' in self.shars[1]:
            self.opens[0] = True
        if '%' in self.shars[1]:
            self.opens[1] = True
        if '^' in self.shars[1]:
            self.opens[2] = True
        self.shar1 = Product(pygame.image.load("1/shar5_3.png").convert_alpha(),
                             (200, 200), "m = 60\nR = 31\nh = 65\n", self.font3,
                             1, 0, 60, 31, 65, open1=True)
        self.shar2 = Product(pygame.image.load("1/shar1_3.png").convert_alpha(),
                             (self.shar1.rect.right + 30, 200),
                             "m = 70\nR = 34\nh = 68\ncoins=10000",
                             self.font3, 2, 10000, 70, 34, 68,
                             open1=self.opens[0])
        self.shar3 = Product(pygame.image.load("1/shar3_3.png").convert_alpha(),
                             (self.shar2.rect.right + 30, 200), 
                             "m = 75\nR = 37\nh = 71\ncoins=30000",
                             self.font3, 3, 30000, 75, 37, 71,
                             open1=self.opens[1])
        self.shar4 = Product(pygame.image.load("1/shar4_3.png").convert_alpha(),
                             (self.shar3.rect.right + 30, 200),
                             "m = 75\nR = 41\nh = 75\ncoins=50000",
                             self.font3, 4, 50000, 75, 41, 75,
                             open1=self.opens[2])
        self.shar_list = [self.shar1, self.shar2, self.shar3, self.shar4]
        pep8_str = "1/menu_button2.png"
        self.fon_menu_button = pygame.image.load(pep8_str).convert_alpha()
        self.qu = Question(self.opens, self.shars, self, self.osn_play,
                           self.shar_list[self.shars[0] - 1])
        self.shar1.add_nomber(int(self.shars[0]))
        self.render_qestion = False
        self.render_qestion_past = self.render_qestion
        self.shop_screen.mo = self.qu.clik_class.m0
        self.shop_screen.r = self.qu.clik_class.r 
        self.shop_screen.maxh = self.qu.clik_class.maxh
        self.ok_change = pygame.image.load("1/ok.png").convert_alpha()   
        pep8_rect = self.ok_change.get_rect(center=self.shar1.rect.center)  
        self.ok_change_rect = pep8_rect
        self.mouse = (-1, -1)

    def repit(self):
        self.shop_button = Button(self.fon_menu_button, (500, 500), "menu")
        self.mouse = (-1, -1)
        
    def render(self):
        screen.blit(self.fon, (0, 0))
        self.render_qestion = False
        if self.shar1.rect.collidepoint(self.mouse):
            self.shar1.add_nomber(1)
            self.qu.clik_class = self.shar1
            self.shars[0] = 1
            print(1.0)
            self.render_qestion = self.shar1.render(self.render_qestion) 
        if self.shar2.rect.collidepoint(self.mouse):
            self.shar1.add_nomber(2) 
            self.qu.clik_class = self.shar2
            self.shars[0] = 2
            self.render_qestion = self.shar2.render(self.render_qestion) 
            print(2.0)
        if self.shar3.rect.collidepoint(self.mouse):
            self.shar1.add_nomber(3)
            self.qu.clik_class = self.shar3
            self.shars[0] = 3
            self.render_qestion = self.shar3.render(self.render_qestion) 
            print(3.0)
        if self.shar4.rect.collidepoint(self.mouse):
            self.shar1.add_nomber(4)  
            self.qu.clik_class = self.shar4
            self.shars[0] = 4
            self.render_qestion = self.shar4.render(self.render_qestion) 
            print(4.0)
        self.shar1.render(self.render_qestion) 
        self.shar2.render(self.render_qestion) 
        self.shar3.render(self.render_qestion) 
        self.shar4.render(self.render_qestion) 
        if self.render_qestion or self.render_qestion_past:
            self.qu.render(self.mouse)
        a = self.shop_button.render(self.mouse, why_screen[0])
        if a == 'menu':
            print(5)
            screen_menu.repit()
            self.shop_screen.who_shar = self.shar1.give_nomber1()
            self.shars[0] = self.shar1.give_nomber()
            self.shop_screen.mo = self.qu.clik_class.m0
            self.shop_screen.r = self.qu.clik_class.r
            self.shop_screen.maxh = self.qu.clik_class.maxh
        why_screen[0] = a
        self.render_qestion_past = self.render_qestion
        
class OverScreen():
    def __init__(self):
        self.fon = pygame.image.load("1/game_over.png").convert()
        self.button_img = pygame.image.load("1/menu_button2.png").convert_alpha()
        self.repit()
        
    def repit(self):
        self.shop_button = Button(self.button_img, (500, 550), "menu")
        self.mouse =(-1, -1)
        
    def render(self):
        screen.blit(self.fon, (0, 0))
        a = self.shop_button.render(self.mouse, why_screen[0])
        if a != 'menu':
            shop_shar.repit() 
            self.mouse =(-1, -1)
            screen_menu.repit()
            osn_play.coins = 0
            shop_shar.shars = [1, '-']   
            shop_shar.opens = [False, False, False]
            shop_shar.shar1.add_nomber(1)
            shop_shar.shar1.add_nomber1(1)
            shop_shar.shar2.open1 = False
            shop_shar.shar3.open1 = False
            shop_shar.shar4.open1 = False
            shop_screen.mo = shop_shar.shar1.m0
            shop_screen.r = shop_shar.shar1.r 
            shop_screen.maxh = shop_shar.shar1.maxh 
            shop_screen.who_shar = 1
            osn_play.who_shar = 1            
        why_screen[0] = a        
        
def game_screen_control(i):
    if why_screen[0] == "menu":
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running[0] = False  
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    screen_menu.mouse = i.pos 
            if i.type == pygame.KEYDOWN:
                if str(i.key) == '13':
                    why_screen[0] = "start_game"
                    shop_screen.repit_function()
        screen.fill((0, 0, 0))
        screen_menu.render()
        
    elif why_screen[0] == "start_game":
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running[0] = False 
            if i.type == pygame.MOUSEBUTTONDOWN:
                shop_screen.get_click(i.pos)  
                shop_screen.down_button = True
            elif i.type == pygame.MOUSEBUTTONUP:
                shop_screen.down_button = '1'
            elif i.type == pygame.KEYDOWN:
                if str(i.key) == '13':
                    why_screen[0] = "game"
                    shop_screen.start_game_screen()
            if shop_screen.down_button:
                shop_screen.mouse_coord = i.pos
        screen.fill((0, 0, 0))
        shop_screen.render()
        
    elif why_screen[0] == "game":
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running[0] = False 
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    if osn_play.peremeshenie_fon == 0:
                        osn_play.extremums = osn_play.extremums_sp
                        osn_play.peremeshenie_fon = 3
                        osn_play.now_time = time()
                elif i.key == pygame.K_HOME:
                    why_screen[0] = "start_game"
                    shop_screen.repit_function()
                elif str(i.key) == '13':
                    if osn_play.peremeshenie_fon == 1:
                        osn_play.fast_rise = True
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    osn_play.get_click(i.pos) 
                elif i.button == 3:
                    Sputnics(sputnics)           
        screen.fill((0, 0, 0))
        osn_play.render() 
    elif why_screen[0] == "shop":
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running[0] = False 
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    shop_shar.mouse = i.pos 
        screen.fill((0, 0, 0))
        shop_shar.render() 
    elif why_screen[0] == "game_over":
        if shop_shar.shars != [0, '-']:
            shop_shar.shars = [0, '-']
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running[0] = False 
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    screen_over.mouse = i.pos 
            elif i.type == pygame.KEYDOWN:
                if str(i.key) == '13':
                    screen_over.mouse = (-1, -1)
                    screen_menu.repit()
                    why_screen[0] = 'menu'
                    osn_play.coins = 0
                    shop_shar.shars = [1, '-']
                    shop_shar.opens = [False, False, False]
                    shop_shar.shar1.add_nomber(1)
                    shop_shar.shar1.add_nomber1(1)
                    shop_shar.shar2.open1 = False
                    shop_shar.shar3.open1 = False
                    shop_shar.shar4.open1 = False
                    shop_screen.mo = shop_shar.shar1.m0
                    shop_screen.r = shop_shar.shar1.r 
                    shop_screen.maxh = shop_shar.shar1.maxh 
                    shop_screen.who_shar = 1
                    osn_play.who_shar = 1
        screen.fill((0, 0, 0))
        screen_over.render()  
    elif why_screen[0] == "learn":
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running[0] = False 
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    learn_class.mouse = i.pos 
            elif i.type == pygame.KEYDOWN:
                if str(i.key) == '13':
                    learn_class.mouse =(-1,-1)
                    screen_menu.repit()
                    why_screen[0] = 'menu'
        screen.fill((0, 0, 0))
        learn_class.render()


fps = 60
try:
    f = open("1/coins.txt", "r")
    coins = int(f.read())
    f.close()
except Exception:
    coins = 0
try:
    f = open("1/shop.txt", "r")
    shars = f.read().split('\n')
    shars[0] = int(shars[0])
    f.close()
except Exception:
    shars = [1, '-']
if shars[0] not in range(1, 5):
    shars[0] = 1
if shars[1] == '-' and shars[0] != 1:
    shars[0] = 1
pygame.init()
screen = pygame.display.set_mode((1000, 600))
fon_start = pygame.image.load("1/login_fon.png").convert()
screen.blit(fon_start, (0, 0))
pygame.display.flip()
screen_menu = Menu()
extremums = [(0, 0)]
extremums_sp = [(0, 0)]
time_max = 0
max_h = 0
sputnics = pygame.sprite.Group()
missiles = pygame.sprite.Group()
prticles = pygame.sprite.Group()
for i in range(choice(range(8, 16))):
    Sputnics(sputnics)
sputnics.sprites()[0].create_group_parts(prticles)
why_screen = ['menu', -1950, 490]
music = Music()
osn_play = PlayClass(max_h, time_max, extremums, extremums_sp,
                     fps, coins, sputnics,
                     missiles, prticles, who_shar=shars[0])
shop_screen = MissileShop(osn_play, 60, extremums, who_shar=shars[0])
shop_shar = ShopShar(shars, osn_play, shop_screen)
screen_over = OverScreen()
learn_class = LearnClass()
running = [True]
print(shars)
clock = pygame.time.Clock()
while running[0]:   
    game_screen_control(0)
    music.render()
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
f = open("1/coins.txt", "w")
f.write(str(osn_play.coins))
f.close()
f = open("1/shop.txt", "w")
print(shop_shar.qu.shars, shop_shar.shars, shars)
str_shars = ''.join(list(set(list(shop_shar.shars[1]))))
f.write(str(shop_shar.shars[0]) + '\n' + str_shars)
f.close()
print()
print(osn_play.extremums)