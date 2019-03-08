# -*- coding: utf8 -*-
# https://icons8.com/animizer/ru/gif-apng-converter - аниматор
from numpy import*
import pygame
import os
from time import sleep, time
from math import pi, degrees
from random import choice,randrange 
from scipy.integrate import odeint
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
            pygame.image.load("1/destr_7.png"),]
    for scale in (5, 10,20):
        fire.append(pygame.transform.scale(fire[1], (scale, scale)))
        fire.append(pygame.transform.scale(fire[2], (scale, scale)))
        fire.append(pygame.transform.scale(fire[5], (scale, scale)))
        fire.append(pygame.transform.scale(fire[6], (scale, scale)))
 
    def __init__(self, pos, dx, dy,radius,alpha,right):
        super().__init__(prticles)
        self.img = choice(self.fire)
        self.image = pygame.transform.rotate(self.img, randrange(0,360))
        self.rect = self.image.get_rect()
        self.radius = radius + choice(range(-50,50))
        self.alpha = alpha + choice(range(-7,7))/100
        self.d_alpha = ((0.02*self.radius/radius)+0.02)/2
        self.rect.center = pos
        self.mask = pygame.mask.from_surface(self.image)
        # гравитация будет одинаковой (значение константы)
        #self.gravity = GRAVITY = 0.5
        self.radius_down = 0
        self.right = right
    def update(self):
        self.alpha +=  self.d_alpha * self.right
        #print(self.alpha, self.d_alpha)
        x = self.radius* cos(self.alpha) + 500 - 60
        y = self.radius * sin(self.alpha) + 1400 + Missiles.osn_object.start_fon_position_for_y +420   - 44 
        self.image = self.img # pygame.transform.scale(self.img, (int(Missiles.masshtab), int(Missiles.masshtab)))
        #print(+ 1400 + Missiles.osn_object.start_fon_position_for_y +420 - 44 )
        
        self.image1 = pygame.transform.rotate(self.image, -degrees(self.alpha)*self.right)#  
        self.mask = pygame.mask.from_surface(self.image1)
        self.rect = self.image1.get_rect()
        self.rect.center = x,y
        
        if self.radius < 830:
            self.radius_down += 1
        if self.radius < 300:
            self.kill()
            #Missiles.osn_object.coins += 100
        #print(self.radius)
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
        #print(Smax)
        #print(self.pul_tupe)
        #print(cell0,cell1)
        self.mass_sprites = [(pygame.image.load("1/pul1_1.png"),(1,1,)),
                             (pygame.image.load("1/pul_a.png"),(5,1,)),
                             (pygame.image.load("1/pul_a2.png"),(3,3,))]# определим его вид
        x0,y0 = self.create_pul(cell0,cell1)
        self.create_tuman()
        
        self.rect = self.image.get_rect(center = (x0,y0)) 
        self.coord_c = self.rect.center
        dx,dy = (self.x1-x0),(self.y1-y0)
        s = (dx**2+dy**2)**0.5
        #print(1)
        self.vx = (15 * (abs(dx)/s))
        self.vy = (15 * (abs(dy)/s))
        self.alpha = arcsin(dx/s)
        if s > Smax:
            s = Smax    
        self.Smax = Smax
        #print(2)
        self.stop_time = s/15
        self.ch = 0
        if dx < 0:
            self.vx *= -1
        if dy < 0:
            self.vy *= -1        

        #print(3)
        if dy>0:
            if dx > 0:
                self.right =-1
                um = 180
            else:
                self.right =-1
                um = 180
        else:
            self.right =1
            um = 0
        #print(4)
        self.degrees_rotare = -degrees(self.alpha)*self.right - um
        self.img = pygame.transform.rotate(self.img, self.degrees_rotare)
        self.tuman = pygame.transform.rotate(self.tuman, self.degrees_rotare)
        self.width,self.height = self.rect.size
        self.become_tuman = Missiles.masshtab
        self.image = self.img
        #print(5)
    def create_pul(self,cell0, cell1):
        #print(77)
        x0,y0 = cell0
        self.x1,self.y1 = cell1   
        #self.img = self.mass_sprites[self.pul_tupe][0]
        self.frames = []
        self.cut_sheet(self.mass_sprites[self.pul_tupe][0], *self.mass_sprites[self.pul_tupe][1])
        self.cur_frame = 0
        self.img = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.img)
        self.image = self.img  
        #print(88)
        return x0,y0 
        
        

 
    def cut_sheet(self, sheet, columns, rows):
        self.rect1 = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        #print(99)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect1.w * i, self.rect1.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect1.size)))
                
    def create_tuman(self):

        
        self.tuman = pygame.Surface((100, 100))
        self.tuman.fill((0,0,0,0))
        self.tuman.set_colorkey((0,0,0,0))
        #self.tuman.set_alpha(200)
        self.tumans = [pygame.image.load("1/tuman1_1.png")]
        self.betta_tuman = self.tumans[0]  
        self.mask_tuman = pygame.mask.from_surface(self.betta_tuman) 
        color_key = self.betta_tuman.get_at((0, 0))
        self.betta_tuman.set_colorkey(color_key)
        self.tuman.blit(self.betta_tuman,(0,0))   
        self.alpha_kanal = 255

    def update(self):
        #print(self.rect)
        if self.ch >= 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.img = self.frames[self.cur_frame]     
            self.image = pygame.transform.rotate(self.img, self.degrees_rotare)
            #print(12)
            if self.ch < self.stop_time  :
                self.become_tuman = Missiles.masshtab
                self.rect.x += self.vx 
                self.rect.y += self.vy
                self.ch += 1
                #print(123)
            else:
                self.ch = -1
                self.coord_c = self.rect.center
                #self.rect.center
                self.become_tuman = Missiles.masshtab/100
                #print(124)
                
        elif self.ch == -1:
            
            #print(132)
            self.img = self.tuman
            self.image = self.tuman
            self.mask = self.mask_tuman
            #xc,yc = self.rect.center
            self.rect = self.img.get_rect(center=self.coord_c)
            
            if Missiles.masshtab+50 >= self.become_tuman:
                self.become_tuman += Missiles.masshtab/100
                if int(self.become_tuman) < 1:
                    self.become_tuman = 1
                self.image = pygame.transform.scale(self.img, (int(self.become_tuman), int(self.become_tuman)))
                self.rect = self.image.get_rect(center=self.coord_c)                
                #print(1321)
            else:
                #print(133)
                self.image = self.img
                self.ch = -2
        else:
            #print(14)
            if self.alpha_kanal <= 0:
                self.kill()
            #self.become_tuman = Missiles.masshtab
            self.tuman.set_alpha(self.alpha_kanal)
            self.tuman.set_colorkey((0,0,0))
            self.alpha_kanal -= 1
            self.mask = self.mask_tuman
            self.image = self.img
        #self.image = self.tuman
        #print(21)
        if pygame.sprite.spritecollideany(self, sputnics):
            for i in range(len(sputnics.sprites())):
                #print(22)
                try:
                    if pygame.sprite.collide_mask(self,sputnics.sprites()[i]): # all_sprites.sprites()[0]
                        self.vy = -self.vy 
                        if self.ch >= 0:
                            particle_count = 15
                            numbers = range(-5, 6)
                            for _ in range(particle_count):
                                Particle(sputnics.sprites()[i].rect.center, 0,0,sputnics.sprites()[i].radius, sputnics.sprites()[i].alpha, sputnics.sprites()[i].right)
                            sputnics.sprites()[i].kill()
                        else:
                            sputnics.sprites()[i].radius_down += 10/(256 - self.alpha_kanal)
                except Exception:
                    print('error sputnics')
                    
        if pygame.sprite.spritecollideany(self, Missiles.group_parts):
            for i in range(len(Missiles.group_parts.sprites())):
                #print(23)
                try:
                    if pygame.sprite.collide_mask(self,Missiles.group_parts.sprites()[i]): # all_sprites.sprites()[0]
                        local_ch = 1
                        self.vy = -self.vy 
                        if self.ch >= 0:
                            Missiles.group_parts.sprites()[i].kill()
                        else:
                            Missiles.group_parts.sprites()[i].radius_down += 10/(256 - self.alpha_kanal)
                except Exception:
                    print('error parts')
        #print('end_update') 
                        
    def redach_mashtab(self, value):
        Missiles.value -= value
        Missiles.masshtab -= (value*100)/750
        
    def create_group_parts(self, group):
        Missiles.group_parts = group

class Sputnics(pygame.sprite.Sprite):
    masshtab = 50
    osn_object = '-'
    group_parts = '-'
    def __init__(self, group):
        self.mass_sprites = [pygame.image.load("1/sputnic3_1.png"),
                             pygame.image.load("1/sputnic2.png"),
                             pygame.image.load("1/sputnic1.png")]# определим его вид
        
        super().__init__(group)
        self.img = choice(self.mass_sprites)
        
        self.mask = pygame.mask.from_surface(self.img)
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.alpha = choice(range(-30, 30,))/10
        self.radius = 1100 + randrange(500)
        self.right = choice([-1,1])
        self.radius_down = 0
        self.masshtab = 0
        self.width,self.height = self.rect.size
        
    def update(self):

        self.alpha += 0.02 * self.right
        x = ((self.radius)* cos(self.alpha) + 500 -66) 
        y = ((self.radius) * sin(self.alpha) + 1400 + Missiles.osn_object.start_fon_position_for_y +420  - 44 )# * 100/Missiles.masshtab  
        self.image = pygame.transform.scale(self.img, (int(Missiles.masshtab), int(Missiles.masshtab)))
        #print(+ 1400 + Missiles.osn_object.start_fon_position_for_y +420 - 44 )
        
        self.image1 = pygame.transform.rotate(self.image, -degrees(self.alpha)*self.right)#  
        self.mask = pygame.mask.from_surface(self.image1)
        self.rect = self.image1.get_rect()
        self.rect.center = x,y
        
        if self.radius < 830:
            self.radius_down += 1
        if self.radius < 300:
            self.kill()
            Missiles.osn_object.coins += 100
        #print(self.radius)
        if self.radius_down != 0:
            if self.radius_down >170:
                particle_count = 15
                # возможные скорости
                numbers = range(-5, 6)
                for _ in range(particle_count):
                    Particle(self.rect.center, x,y, self.radius, self.alpha, self.right) 
                Missiles.group_parts.sprites()[0].osn_object_function(Missiles.osn_object)
                self.kill()
            self.radius -= self.radius_down/10
            self.radius_down -= self.radius_down/10            
       
    def redach_mashtab(self, value):
        Missiles.masshtab -= (value*100)/750    
       
    def osn_object_function(self, obj):
        Missiles.osn_object = obj
        
    def create_group_parts(self, group):
        Missiles.group_parts = group
        
        
class PlayClass():
    def __init__(self,max_h,time_max,extremums, extremums_sp, fps,coins,sputnics,missiles,prticles, who_shar=1):
        self.very_max = 65482
        self.radius_shar = 31
        self.create_class(sputnics,missiles,prticles)
        self.create_init_tools(fps)
        self.delete_this_ch = 0
        self.download_convas()
        self.now_start(who_shar1 = who_shar)
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
        self.start_fon_position_for_y = -1700  #-400 -1400 --------------------------------------------------------------
        self.start_fon_position_for_x = -500
        self.start_fon_position_for_player_y = -1850 # -----------------------------------------------------
        self.start_fon_position_for_player_x = -500
        self.for_player_step_x = -2
        self.start_fon_position_for_x_kostil = 0
        self.start_fon_position_for_y_kostil = 0
        
    def download_convas(self):
        self.fon = pygame.image.load("1/fon4.png").convert()
        self.shar = pygame.image.load("1/shar1_2.png").convert_alpha()
        self.pul1_how = pygame.image.load("1/pul1_how.png").convert_alpha()
        self.coin_image = pygame.image.load("1/coin.png").convert_alpha()
        self.coin_image_rect = self.coin_image.get_rect(centery=75, left=10)
        self.surf = pygame.Surface((2000, 2500), pygame.SRCALPHA)
        self.surf.fill((0,0,0,0)) 
        
    def create_shar(self, who_shar=1): 
        self.who_shar = who_shar
        self.shar = pygame.image.load("1/shar"+str(self.who_shar)+"_2.png").convert_alpha()        
        self.shar1 = self.shar.copy()
        self.shar1_rect = self.shar1.get_rect(centerx=500,bottom=470)
        self.shar1_rect_impuls = self.shar1_rect
        self.x, self.y = self.shar1_rect.topleft
        self.x_im, self.y_im = self.x, self.y
        self.shar_mashtab_step_for_start_x = 116
        self.shar_mashtab_step_for_start_y = 116 
        self.bufer_y = 0
        self.speed = 0
        self.how_many_pul = 0
        
        
    def create_class(self,sputnics,missiles,prticles):
        self.sputnics = sputnics
        self.missiles = missiles
        self.prticles = prticles
        Sputnics(self.sputnics)        
        Missiles(self.missiles,(-100,-100),(-201,-201),1,250)
        self.missiles.sprites()[0].create_group_parts(self.prticles)
        #self.missiles.sprites()[0].kill()
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
        self.key_down,self.key_up = False, False
        self.chetchic1 = 0
        self.now_time = time()
        self.speed_x, self.speed_y = 0,0
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
            print(max_h_fiying)
            self.max_h_fiying_index = self.extremums.index(max_h_fiying)
            self.time_max_fliting, self.max_h_fiying = max_h_fiying
        except Exception as e:
            print(e)
            
        
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
            #print(e)

    def get_cell(self, cort):
        x, y = pygame.mouse.get_pos()
        return x, y #(x, y,)
    
    def on_click(self, rr,cell):
        if self.how_many_pul > 0:
            Missiles(self.missiles,(self.shar1_rect_impuls.center),cell, self.tupe_pul[0][0], Smax=self.tupe_pul.pop(0)[1])
            #print('----', self.tupe_pul[0])
            self.m -= self.pul_mas
            self.impuls_speed(self.missiles.sprites()[-1])
            self.how_many_pul -=1
            
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
        #print(self.delete_this_ch)
        #self.max_h_fiying = max(self.extremums, key=lambda i: i[1])
        #print(self.max_h_fiying, self.max_h_fiying_index)
        if self.peremeshenie_fon == 3 and self.start_fon_position_for_y - (self.shar1_rect.top) < -2170:
            self.speed = 0
            why_screen[0] = "start_game"
            shop_screen.repit_function()
            #print(2)
            #print("start_game")
        #elif self.ch2+1 < len(self.extremums):
        
        #print('++++++++++++++++++++++_________________________')
        if self.fast_rise or (self.peremeshenie_fon == 1  and (self.extremums[(self.ch3 if self.ch3 >= 0 else 0)][1]) > self.max_h_fiying - 1500): # m_time/self.fps * 5 >= (self.time_max_fliting/(31)): # 
            self.peremeshenie_fon = 0
            if self.fast_rise:
                
                self.ch2 = self.max_h_fiying_index - 1
                
                #print('--')
            #print('777777777777777')
        if self.peremeshenie_fon != 3:
            time_ex,h = self.extremums[self.ch2+1]
            if m_time  >= time_ex or self.fast_rise:#/(self.fps*10): # self.fps * 5
                if self.fast_rise:
                    self.fast_rise = False
                    self.start_fon_position_for_y += self.speed * (time_ex - m_time)*30
               #print('-----------------========== ', self.peremeshenie_fon)
                self.ch2 += 1
                self.ch3 += 1
            
                new_t,new_h = self.extremums[self.ch2+1]
                if m_time == 0:
                    m_time = ((time() - self.now_time))
                self.speed =  ((new_h - h)/(new_t - m_time))/(self.fps * 20)
        else:
            self.speed = -1.7
            #print((new_h - h), h, time_ex)
            
                
    def impuls_speed(self, pul):
        self.speed_x -= (self.pul_mas*pul.vx)/(self.m)
        self.speed_y -= (self.pul_mas*pul.vy)/(self.m)
        #pul.alpha
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
        
        if True :	
            self.fon_copy = self.fon
            m_time = int((time() - self.now_time))
            try:
                self.speed_raschet(m_time*2)
            except Exception as e:
                print(e)
            #print(self.start_fon_position_for_y, self.start_fon_position_for_y - (self.shar1_rect.y), self.speed, m_time, self.shar1_rect)
            if m_time <= 200:
                
                
                if self.peremeshenie_fon in [1, 2, 3]:
                    #print('909090909090909')
                    if False and (self.y <= 0) or ( 2200 - self.y >= self.max_h_fiying - 50): 
                        self.peremeshenie_fon = 0
                        #print('00000000000000000000')
                    else:
                        self.start_fon_position_for_y += self.speed
                        #self.start_fon_position_for_player_y += self.speed
                        #self.y -= self.speed
                        #print("+++++++++++++++++++++++++++++++++++++++++")
                if self.peremeshenie_fon == 0:
                    self.y -= self.speed

            self.key_button_control()
            if False:
                if self.chetchic1 < 500: #self.fon_mashtab_step_for_start_x > 1500:     
                    k = 3
                    self.chetchic1 +=4 * k
                    self.fon_mashtab_step_for_start_x -= 4* k
                    self.fon_mashtab_step_for_start_y -= 4* k
                    self.shar_mashtab_step_for_start_x -= 0.232 * k*2
                    self.shar_mashtab_step_for_start_y -= 0.232   * k  *2              
                    self.x += self.for_player_step_x
                    self.start_fon_position_for_x +=2* k
                    self.start_fon_position_for_y+=1* k
                    self.start_fon_position_for_player_x +=2
                    self.start_fon_position_for_player_y += 1* k
                    self.surf = pygame.transform.smoothscale(self.fon, (int(self.fon_mashtab_step_for_start_x),int(self.fon_mashtab_step_for_start_y)))   
                    self.shar1 = pygame.transform.smoothscale(self.shar, (int(self.shar_mashtab_step_for_start_x),int(self.shar_mashtab_step_for_start_y)))
                    try:
                        self.sputnics.sprites()[0].redach_mashtab(4 )
                        self.missiles.sprites()[0].redach_mashtab(4 )
                    except Exception:
                        pass                    
                else:
                    self.surf = self.fon #pygame.transform.smoothscale(self.fon, (int(self.fon_mashtab_step_for_start_x),int(self.fon_mashtab_step_for_start_y))) 
                    self.shar1 = self.shar # pygame.transform.smoothscale(self.shar, (int(self.shar_mashtab_step_for_start_x),int(self.shar_mashtab_step_for_start_y)))
            else:
                self.surf = self.fon #pygame.transform.smoothscale(self.fon, (int(self.fon_mashtab_step_for_start_x),int(self.fon_mashtab_step_for_start_y))) 
                self.shar1 = self.shar                
            if self.chetchic1 >= 490 and self.peremeshenie_fon == 1:
                self.peremeshenie_fon = 0            
            #print('self.peremeshenie_fon', self.peremeshenie_fon)
            if self.start_fon_position_for_x_kostil != 0:
                #print('==================')
                self.start_fon_position_for_x += self.start_fon_position_for_x_kostil
                self.start_fon_position_for_y += self.start_fon_position_for_y_kostil
                try:
                    self.sputnics.sprites()[0].redach_mashtab(self.start_fon_position_for_x_kostil)
                    self.missiles.sprites()[0].redach_mashtab(self.start_fon_position_for_x_kostil)
                except Exception:
                    pass
            self.bufer_y = self.speed
            
            screen.blit(self.surf, (self.start_fon_position_for_x,self.start_fon_position_for_y))#self.surf1.blit(self.fon_surf, (0,0))
            self.start_fon_position_for_x_kostil = 0
            self.start_fon_position_for_y_kostil = 0   

            self.x_im += self.speed_x
            self.y_im += self.speed_y
            self.speeds_control()
            self.shar1_rect.topleft = self.x_im, self.y
            self.shar1_rect_impuls.topleft = self.x_im, self.y_im
            #print( self.shar1_rect, self.shar1_rect_impuls)
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
            text = font.render(str(self.how_many_pul), 1, (100,100 , 255))
            text_rect = text.get_rect(centery = 40,left = 50)
            pul1_how_tect = self.pul1_how.get_rect(centery = 40,left = 10)
            coins_text = font.render(str(self.coins), 1, (100,100 , 255))
            coins_text_rect = coins_text.get_rect(centery = 75, left = 50)
            screen.blit(self.pul1_how, pul1_how_tect) 
            screen.blit(self.coin_image, self.coin_image_rect)
            screen.blit(text, text_rect)
            screen.blit(coins_text, coins_text_rect)
            #print(len(self.sputnics.sprites()))
        self.ch1 += 1
        

class Button():
    def __init__(self, image, cell, what_return):
        self.image_button = image
        self.rect_button = self.image_button.get_rect(center = (cell))#
        self.what_return = what_return
    def render(self,cell,otvet_no):
        screen.blit(self.image_button, self.rect_button)
        if self.rect_button.collidepoint(cell):
            return self.what_return
        else:
            return otvet_no

class Menu():
    def __init__(self):
        self.fon = pygame.image.load("1/fon_menu.png").convert()
        self.start_button_img = pygame.image.load("1/start_button.png").convert_alpha()
        self.start_button = Button(self.start_button_img,(500,300),"start_game")
        self.shop = pygame.image.load("1/shop_button2.png").convert_alpha()
        self.shop_button = Button(self.shop,(500,450),"shop")
        self.mouse = (-1,-1)
    def repit(self):
        self.shop_button = Button(self.shop,(500,450),"shop")
        self.start_button = Button(self.start_button_img,(500,300),"start_game")
        self.mouse =(-1,-1)
    def render(self):
        screen.blit(self.fon,(0,0))
        a = self.shop_button.render(self.mouse, why_screen[0])
        if a != 'menu':
            shop_shar.repit()  
        why_screen[0] = a
        a = self.start_button.render(self.mouse, why_screen[0])
        if a != 'menu':
            shop_screen.repit_function()
        why_screen[0] = a        
        #print('why_screen[0]', why_screen[0])

class Board:
    def __init__(self, width, height,x,y,tupe, coins, m=10, Smax=250):
        #self.down_button = False
        self.width = width
        self.height = height
        self.x, self.y = x,y
        self.tupe = tupe
        self.prise = coins
        self.m = m
        self.Smax = Smax
        x,y = 0,0
        self.pul = pygame.image.load("1/pul1_1x1.png").convert_alpha()#
        self.yach = pygame.image.load("1/one_yacheyka.png").convert()#
        
        rect = self.yach.get_rect()
        self.board = [ [self.yach.get_rect(topleft = (j*rect.width + self.x, i*rect.height + self.y)) for i in range(height)][::] for j in range(width)]
        self.board_bul = [ [ [None,(j*rect.width + self.x, i*rect.height + self.y),tupe, coins,self.m,self.Smax].copy() for i in range(height)][::] for j in range(width)]
        self.board_rect = pygame.Rect(self.x, self.y, self.width*rect.width, self.height*rect.height)
        self.left = 110
        self.top = 110
        self.cell_size = 30
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        
    def get_click(self, mouse_pos):
        if self.board_rect.collidepoint(mouse_pos): 
            for i in range(len(self.board_bul)):
                for j in range(len(self.board_bul[i])):
                    if str(type(self.board_bul[i][j][1])) == "<class 'pygame.Rect'>":
                        if self.board_bul[i][j][1].collidepoint(mouse_pos): 
                            #print('---------',mouse_pos,i,j)
                            cell = self.get_cell(mouse_pos)
                            self.on_click(self, cell)
                            return (i,j,self.board_bul[i][j][0],self.board_bul[i][j][1])
        return None
        
    def get_cell(self, cort):
        x, y = pygame.mouse.get_pos()
        x, y = (x - self.left)//self.cell_size, (y - self.top)//self.cell_size
        # print(x, y)
        if (x >= 0 and x <= self.width) and (y >= 0 and y <= self.height):
            return (x, y,)
    
    def on_click(self, obg, cell):
        if cell:
            pass
    def render(self):
        
        for i in range(self.width):
            for j in range(self.height):
                screen.blit(self.yach , self.board[i][j])
                if str(type(self.board_bul[i][j][1])) == "<class 'pygame.Rect'>":
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
        self.coin_rect1 = self.coin_image.get_rect(bottom = 50, centerx = 475)
        self.coin_rect2 = self.coin_image.get_rect(bottom = 50, centerx = 525)
        self.coin_rect3 = self.coin_image.get_rect(centery=45, left=10)
        self.fon = pygame.image.load("1/fon4.png").convert()
        self.start_button_img = pygame.image.load("1/start_button.png").convert_alpha()
        self.menu_button_img = pygame.image.load("1/menu_button.png").convert_alpha()
        self.shar = pygame.image.load("1/shar"+str(self.who_shar)+"_2.png").convert_alpha()
        self.shar_rect = self.shar.get_rect(left=470, bottom=why_screen[2])
        self.texr_fon = pygame.image.load("1/text3.png").convert_alpha()
        self.start_button = Button(self.start_button_img,(700,450),"game") 
        self.menu_button = Button(self.menu_button_img,(700,530),"menu")   
        self.extremums = extremums
        self.board_bag = Board(4, 5,100,50,-1, 0)
        self.board_shop = Board(1, 5,400,50,1, 0)   
        self.board_shop2 = Board(1, 5,450, 50, 2, 10, Smax=400) 
        self.board_shop3 = Board(1, 5,500,50,3, 15, m=5)
        self.pul = pygame.image.load("1/pul1_1x1.png").convert_alpha()#
        self.pul5 = pygame.image.load("1/pul1_1x5.png").convert_alpha()#
        self.pul10 = pygame.image.load("1/pul1_1x10.png").convert_alpha()#
        self.pul20 = pygame.image.load("1/pul1_1x20.png").convert_alpha()#
        self.pulall = pygame.image.load("1/pul1_1xall.png").convert_alpha()#
        self.pul_2 = pygame.image.load("1/pul2_1x1.png").convert_alpha()#
        self.pul5_2 = pygame.image.load("1/pul2_1x5.png").convert_alpha()#
        self.pul10_2 = pygame.image.load("1/pul2_1x10.png").convert_alpha()#
        self.pul20_2 = pygame.image.load("1/pul2_1x20.png").convert_alpha()#
        self.pulall_2 = pygame.image.load("1/pul2_1xall.png").convert_alpha()#  
        self.pul_3 = pygame.image.load("1/pul3_1.png").convert_alpha()#
        self.pul5_3 = pygame.image.load("1/pul3_1x5.png").convert_alpha()#
        self.pul10_3 = pygame.image.load("1/pul3_1x10.png").convert_alpha()#
        self.pul20_3 = pygame.image.load("1/pul3_1x20.png").convert_alpha()#
        self.pulall_3 = pygame.image.load("1/pul3_1xall.png").convert_alpha()        
        self.down_button = False
        self.mouse_coord = -1,-1
        self.mouse_img, self.mouse_img_rect = None, None#self.pul, self.pul.get_rect()

        self.ch = 0
        self.tupe_pul = -1
        self.board_shop.board_bul[0][0][:2:] = [self.pulall, self.pulall.get_rect(topleft=self.board_shop.board_bul[0][0][1])] # ,*self.board_shop.board_bul[0][0][2::])
        self.board_shop.board_bul[0][1][:2:] = [self.pul20, self.pul20.get_rect(topleft=self.board_shop.board_bul[0][1][1])] # ,*self.board_shop.board_bul[0][0][2::])
        self.board_shop.board_bul[0][2][:2:] = [self.pul10, self.pul10.get_rect(topleft=self.board_shop.board_bul[0][2][1])] # ,*self.board_shop.board_bul[0][0][2::])
        self.board_shop.board_bul[0][3][:2:] = [self.pul5, self.pul5.get_rect(topleft=self.board_shop.board_bul[0][3][1])] # ,*self.board_shop.board_bul[0][0][2::])
        self.board_shop.board_bul[0][4][:2:] = [self.pul, self.pul.get_rect(topleft=self.board_shop.board_bul[0][4][1])] # ,*self.board_shop.board_bul[0][0][2::])
        
        self.board_shop2.board_bul[0][0][:2:] = [self.pulall_2, self.pulall_2.get_rect(topleft=self.board_shop2.board_bul[0][0][1])] # ,*self.board_shop2.board_bul[0][0][2::])
        self.board_shop2.board_bul[0][1][:2:] = [self.pul20_2, self.pul20_2.get_rect(topleft=self.board_shop2.board_bul[0][1][1])] # ,*self.board_shop2.board_bul[0][1][2::])
        self.board_shop2.board_bul[0][2][:2:] = [self.pul10_2, self.pul10_2.get_rect(topleft=self.board_shop2.board_bul[0][2][1])] # ,*self.board_shop2.board_bul[0][2][2::])
        self.board_shop2.board_bul[0][3][:2:] = [self.pul5_2, self.pul5_2.get_rect(topleft=self.board_shop2.board_bul[0][3][1])] # ,*self.board_shop2.board_bul[0][3][2::])
        self.board_shop2.board_bul[0][4][:2:] = [self.pul_2, self.pul_2.get_rect(topleft=self.board_shop2.board_bul[0][4][1])] # ,*self.board_shop2.board_bul[0][4][2::])    
        
        self.board_shop3.board_bul[0][0][:2:] = [self.pulall_3, self.pulall_3.get_rect(topleft=self.board_shop3.board_bul[0][0][1])] # ,*self.board_shop3.board_bul[0][0][2::])
        self.board_shop3.board_bul[0][1][:2:] = [self.pul20_3, self.pul20_3.get_rect(topleft=self.board_shop3.board_bul[0][1][1])]# ,*self.board_shop3.board_bul[0][1][2::])
        self.board_shop3.board_bul[0][2][:2:] = [self.pul10_3, self.pul10_3.get_rect(topleft=self.board_shop3.board_bul[0][2][1])] # ,*self.board_shop3.board_bul[0][2][2::])
        self.board_shop3.board_bul[0][3][:2:] = [self.pul5_3, self.pul5_3.get_rect(topleft=self.board_shop3.board_bul[0][3][1])] # ,*self.board_shop3.board_bul[0][3][2::])
        self.board_shop3.board_bul[0][4][:2:] = [self.pul_3, self.pul_3.get_rect(topleft=self.board_shop3.board_bul[0][4][1])] # ,*self.board_shop3.board_bul[0][4][2::])        
        
    def get_click(self, mouse_pos):
        a = None
        if self.board_shop.board_rect.collidepoint(mouse_pos):
            a = self.board_shop.get_click(mouse_pos)
            self.tupe_pul = 1
            #self.board_shop.down_button = self.down_button
        elif self.board_shop2.board_rect.collidepoint(mouse_pos):
            self.tupe_pul = 2
            a = self.board_shop2.get_click(mouse_pos)  
        elif self.board_shop3.board_rect.collidepoint(mouse_pos):
            self.tupe_pul = 3
            a = self.board_shop3.get_click(mouse_pos)    
        elif self.board_bag.board_rect.collidepoint(mouse_pos):
            pass
            #a = self.board_bag.get_click(mouse_pos)
            #self.board_bag.down_button = self.down_button
        if a:
            x,y,self.mouse_img,self.mouse_img_rect = a
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
            #if self.down_button
            #if self.down_button:
    def get_cell(self, cort):
        x, y = pygame.mouse.get_pos()
        x, y = (x - self.left)//self.cell_size, (y - self.top)//self.cell_size
        # print(x, y)
        if (x >= 0 and x <= self.width) and (y >= 0 and y <= self.height):
            return (x, y,)
    
    def on_click(self, obg, cell):
        if cell:
            pass    
    def repit_function(self):
        self.start_button = Button(self.start_button_img,(700,450),"game")
        self.menu_button = Button(self.menu_button_img,(700,530),"menu")
        self.down_button = False
        self.mouse_coord = -1,-1
        self.mouse_img, self.mouse_img_rect = None, None#self.pul, self.pul.get_rect()
        self.mas_pul = 0
        self.ch = 0     
        self.board_bag = Board(4, 5,100,50,-1, 0)
        #self.who_shar
        self.shar = pygame.image.load("1/shar"+str(self.who_shar)+"_2.png").convert_alpha()
        self.shar_rect = self.shar.get_rect(left=470, bottom=why_screen[2])
    def render(self):
        screen.blit(self.fon,(-500, why_screen[1]))
        screen.blit(self.shar, self.shar_rect)
        self.board_bag.render()
        self.board_shop.render()
        self.board_shop2.render()
        self.board_shop3.render()
        font = pygame.font.Font(None, 34)
        font2 = pygame.font.Font(None, 20)
        font3 = pygame.font.Font(None, 20)
        #text = font.render(str(self.how_many_pul), 1, (100,100 , 255))
        #text_rect = text.get_rect(centery = 40,left = 50)
        #pul1_how_tect = self.pul1_how.get_rect(centery = 40,left = 10)
        coins_text = font.render(str(self.osnov_class.coins), 1, (100, 100, 255))
        coins_text_rect = coins_text.get_rect(centery = 45, left = 50)   
        price1 = font2.render(str(10), 1, (0, 0, 255))
        price1_rect = price1.get_rect(center = self.coin_rect1.center)
        price2 = font2.render(str(15), 1, (0, 0, 255))
        price2_rect = price2.get_rect(center = self.coin_rect2.center)        
        screen.blit(self.coin_image, self.coin_rect1)
        screen.blit(self.coin_image, self.coin_rect2)
        screen.blit(self.coin_image, self.coin_rect3)
        screen.blit(coins_text, coins_text_rect)  
        screen.blit(price1,price1_rect)
        screen.blit(price2,price2_rect)
        screen.blit(self.texr_fon, (200,390))
        m_shar = font3.render("Масса шара " + str(self.mo), 1, (255, 255, 255))
        fly = font3.render("Max высота без груза " + str(self.maxh) + 'т.', 1, (255, 255, 255))
        m = font3.render('Mасса ' + str(self.mo + self.mas_pul), 1, (255, 255, 255))
        radius = font3.render('Радиус шара ' + str(self.r), 1, (255, 255, 255))
        screen.blit(m_shar, (240,440))
        screen.blit(fly, (240,460))
        screen.blit(m, (240,480))
        screen.blit(radius, (240,500))
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
                                self.board_bag.board_bul[i][j] = class_shop.board_bul[0][4][::] #[class_shop.board_bul[0][4][0], self.pul.get_rect(topleft = self.board_bag.board_bul[i][j][1]), self.tupe_pul, *class_shop.board_bul[0][4][3::]]# 
                                #print(class_shop.board_bul[0][4])
                                self.board_bag.board_bul[i][j][1] = self.pul.get_rect(topleft = coord)
                                #print(self.board_bag.board_bul[i][j])
                                self.mas_pul += class_shop.m
                                self.ch -= 1
                            except Exception as e:
                                print('erorr pul_render', e)
                        if self.ch <=0 or self.osnov_class.coins <= 0:
                            break
                    if self.ch <=0 or self.osnov_class.coins <= 0:
                        break
        
        elif not(self.down_button):
            self.mouse_img = None 
        if self.mouse_img:
            screen.blit(self.mouse_img,self.mouse_coord)
        
        a = self.start_button.render(self.mouse_coord, why_screen[0])      
        if a == "game":
            ch = 0
            self.osnov_class.tupe_pul = []
            local_m = []
            for i in range(len(self.board_bag.board_bul)):
                for j in range(len(self.board_bag.board_bul[i])): 
                    if self.board_bag.board_bul[i][j][0]:
                        self.osnov_class.tupe_pul.append([self.board_bag.board_bul[i][j][2],self.board_bag.board_bul[i][j][5]])
                        local_m.append(self.board_bag.board_bul[i][j][4])
                        ch += 1
            mo = int(self.mo + sum(local_m) )#итоговая мвсса шара
            print('=====', self.osnov_class.tupe_pul)
            try:
                masss = importlib.import_module('mass_' + str(mo) + '_' + str(self.r))
            except Exception:
                import make_massivs
                make_massivs.func(mo, self.r)
                f = open('mass_' + str(mo) + '_' + str(self.r) + '.py', 'r')
                f.close()
                masss = importlib.import_module('mass_' + str(mo)+ '_' + str(self.r))
                
            masss = importlib.import_module('mass_' + str(mo)+ '_' + str(self.r))
            print(mo)
            print(self.r)
            print(masss.mass)
            self.extremums = masss.mass[::]
            self.extremums_sp = masss.mass_sp[::]
            self.osnov_class.tupe_pul.sort(reverse=True, key=lambda i: i[0])
            print(self.extremums)
            #self.osnov_class.tupe_pul =
            self.osnov_class.now_start(who_shar1=self.who_shar) # self.who_shar = who_shar1
            self.osnov_class.restart(ch, masss.max_h, masss.time_max, self.extremums, self.extremums_sp)
        why_screen[0] = a
        a = self.menu_button.render(self.mouse_coord, why_screen[0])
        if a == "menu":
            screen_menu.repit()
        why_screen[0] = a
def print_text(string,topleft1,font=None, font_size=10,return_surf=False):
    surf = pygame.Surface((200, 200), pygame.SRCALPHA)
    surf.fill((0,0,0,0))
    if font:
        pass
    else:
        font = pygame.font.Font(None, font_size)
    str_list = string.split('\n')
    post_text_rect = pygame.Rect(-1,30,1,1)
    for i in str_list:  
        text = font.render(i, 1, (255, 255, 255))
        text_rect = text.get_rect(top=post_text_rect.bottom, left=post_text_rect.left)
        if return_surf:
            pass
        else:
            surf.blit(text, text_rect)
            post_text_rect = text_rect.copy()
    
    return surf
class Product():
    nomber = 0
        
    def __init__(self, img, topleft1, text, font1, num, prise, m0, r, h, open1=False):
        self.ok_change = [pygame.image.load("1/ok.png").convert_alpha()   ]    
        self.img = img
        self.num = num
        self.open1 = open1
        self.prise = prise
        self.m0 = m0
        self.r = r
        self.maxh = h
        if self.open1:
            self.prise = 0
        self.rect = self.img.get_rect(topleft = topleft1)
        self.text = print_text(text, self.rect.topleft, font=font1)
        self.text_rect = self.text.get_rect(topleft=(self.rect.left, self.rect.bottom))
        self.surf_black1 = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.surf_black1.fill((0,0,0,150))
        self.ok_change_rect = self.ok_change[0].get_rect(center = self.rect.center)
        
    def render(self, render_qestion):
        screen.blit(self.img, self.rect)
        screen.blit(self.text, self.text_rect)
        if not(self.open1):
            screen.blit(self.surf_black1, self.rect )
        else:
            pass
            #render_qestion = False
        if Product.nomber == self.num:
            if self.open1:
                screen.blit(self.ok_change[0], self.ok_change_rect)
            else:
                #Product.nomber = 1
                return True
        return render_qestion
    def add_nomber(self, num):
        Product.nomber = num
    def give_nomber(self):
        return Product.nomber
class Question():
    def __init__(self,mass,shars, shop_class, osn_play, shar1_class):
        self.osn_play = osn_play
        self.opens = mass
        self.shars = shars
        self.shop_class = shop_class
        self.fon = pygame.image.load("1/qu.png")
        self.fon_rect = self.fon.get_rect()
        self.answer_qu = ['see']
        self.clik_class = shar1_class 
        self.no_button = Button(pygame.image.load("1/qu_no.png"),(self.fon_rect.left + 90, self.fon_rect.top+ 138),  'close')
        self.yes_button = Button(pygame.image.load("1/qu_yes.png"),(self.fon_rect.left + 210, self.fon_rect.top+ 138),  'yes')
    def render(self, mouse):
        screen.blit(self.fon,(0,0))
        a = self.no_button.render(mouse, self.answer_qu[0])
        #print(a)
        if a == 'close':
            #print('--')
            self.shop_class.render_qestion = False
            a = 'see'
        self.answer_qu[0] = a
        if self.osn_play.coins >= self.clik_class.prise:
            a = self.yes_button.render(mouse, self.answer_qu[0])
            #print('+++++', self.opens, self.shars, a)
            if a == 'yes':
                #print('--')
                self.shop_class.render_qestion = False
                self.clik_class.open1 = True
                
                self.osn_play.coins -= self.clik_class.prise
                f = self.clik_class.give_nomber() - 2
                if f >= 0:
                    self.opens[f] = True
                self.clik_class.prise = 0
                print(self.opens, f , self.clik_class.give_nomber())
                self.shars[0] = self.clik_class.give_nomber()
                if self.opens[0]:
                    self.shars[1] += '$'
                if self.opens[1]:
                    self.shars[1] += '%'
                if self.opens[2]:
                    self.shars[1] += '^' 
                #print('=====--------------------------------------')
                a = 'see'
            self.answer_qu[0] = a           
class ShopShar():
    def __init__(self,shars, osn_play, shop_screen):
        self.shop_screen = shop_screen
        self.osn_play = osn_play
        self.shars = shars
        self.opens = [False,False,False]
        #self.qu = Question(self.opens,self.shars, self, self.osn_play)
        self.fon = pygame.image.load("1/shop_fon.jpg").convert()
        self.font3 = pygame.font.Font(None, 20)
        
        #self.opens = [False,False,False]
        if '$' in self.shars[1]:
            self.opens[0] = True
        if '%' in self.shars[1]:
            self.opens[1] = True
        if '^' in self.shars[1]:
            self.opens[2] = True
        print(self.opens, self.shars)
        self.shar1 = Product(pygame.image.load("1/shar5_3.png").convert_alpha(), (200,200), "m = 60\nR = 31\nh = 65", self.font3, 1, 0, 60, 31, 65, open1=True)
        self.shar2 = Product(pygame.image.load("1/shar1_3.png").convert_alpha(), (self.shar1.rect.right + 30, 200), "m = 70\nR = 34\nh = 68", self.font3, 2, 10000, 70, 34, 68, open1=self.opens[0])
        self.shar3 = Product(pygame.image.load("1/shar3_3.png").convert_alpha(), (self.shar2.rect.right + 30, 200), "m = 75\nR = 37\nh = 71", self.font3, 3, 30000, 75, 37, 71, open1=self.opens[1])
        self.shar4 = Product(pygame.image.load("1/shar4_3.png").convert_alpha(), (self.shar3.rect.right + 30, 200), "m = 75\nR = 41\nh = 75", self.font3, 4, 50000, 75, 41, 75, open1=self.opens[2])
        self.shar_list = [self.shar1,self.shar2,self.shar3, self.shar4]
        self.fon_menu_button = pygame.image.load("1/menu_button.png").convert_alpha()
        self.qu = Question(self.opens,self.shars, self, self.osn_play, self.shar_list[self.shars[0] - 1])
        self.shar1.add_nomber(int(self.shars[0]))
        print('--', self.shars)
        self.render_qestion = False
        self.shop_screen.mo = self.qu.clik_class.m0
        self.shop_screen.r = self.qu.clik_class.r 
        self.shop_screen.maxh = self.qu.clik_class.maxh
        #self.shar2_rect = self.shar2.get_rect(topleft = (self.shar1.rect.right + 30, 200))
        #self.shar3_rect = self.shar3.get_rect(topleft = (self.shar2_rect.right + 30, 200))
        #self.shar4_rect = self.shar4.get_rect(topleft = (self.shar3_rect.right + 30, 200))
        
        #self.surf_black2 = pygame.Surface(self.shar2_rect.size, pygame.SRCALPHA)
        #self.surf_black3 = pygame.Surface(self.shar3_rect.size, pygame.SRCALPHA)
        #self.surf_black4 = pygame.Surface(self.shar4_rect.size, pygame.SRCALPHA)
         
        #self.surf_black2.fill((0,0,0,150)) 
        #self.surf_black3.fill((0,0,0,150)) 
        #self.surf_black4.fill((0,0,0,150)) 
        
        self.ok_change = pygame.image.load("1/ok.png").convert_alpha()   
        self.ok_change_rect = self.ok_change.get_rect(center = self.shar1.rect.center)        
        
        
        #self.m1 = self.font3.render(, 1, (255, 255, 255))
        #self.m2 = print_text("m = 70\nR = 34\nh = 68", self.shar2_rect.topleft, font=self.font3)   #1, (255, 255, 255))
        #self.m3 = print_text("m = 75\nR = 37\nh = 71", self.shar3_rect.topleft, font=self.font3)  #1, (255, 255, 255))
        #self.m4 = print_text("m = 75\nR = 41\nh = 75", self.shar4_rect.topleft, font=self.font3)  #1, (255, 255, 255))
        
        #self.m2_rect = self.m2.get_rect(topleft=(self.shar2_rect.left, self.shar2_rect.bottom))
        #self.m3_rect = self.m3.get_rect(topleft=(self.shar3_rect.left, self.shar3_rect.bottom))
        #self.m4_rect = self.m4.get_rect(topleft=(self.shar4_rect.left, self.shar4_rect.bottom))
        
        self.mouse = (-1,-1)
        
          
    def repit(self):
        self.shop_button = Button(self.fon_menu_button,(500,450),"menu")
        self.mouse = (-1,-1)
    def render(self):
        screen.blit(self.fon,(0,0))
        if self.shar1.rect.collidepoint(self.mouse):
            self.shar1.add_nomber(1)
            self.qu.clik_class = self.shar1
            self.shars[0] = 1
            print(1.0)
        if self.shar2.rect.collidepoint(self.mouse):
            self.shar1.add_nomber(2) 
            self.qu.clik_class = self.shar2
            self.shars[0] = 2
            print(2.0)
        if self.shar3.rect.collidepoint(self.mouse):
            self.shar1.add_nomber(3)
            self.qu.clik_class = self.shar3
            self.shars[0] = 3
            print(3.0)
        if self.shar4.rect.collidepoint(self.mouse):
            self.shar1.add_nomber(4)  
            self.qu.clik_class = self.shar4
            self.shars[0] = 4
            print(4.0)
        print(self.qu.clik_class.give_nomber())
        print(self.render_qestion)
        self.render_qestion = self.shar1.render(self.render_qestion)
        self.render_qestion = self.shar2.render(self.render_qestion)
        self.render_qestion = self.shar3.render(self.render_qestion)
        self.render_qestion = self.shar4.render(self.render_qestion) 
        print(self.render_qestion)
        #print(self.render_qestion)
        if self.render_qestion:
            self.qu.render(self.mouse)
        #print(self.render_qestion)
        #screen.blit(self.shar2, self.shar2_rect)
        #screen.blit(self.shar3, self.shar3_rect)
        #screen.blit(self.shar4, self.shar4_rect)
        #screen.blit(self.m1, self.m1_rect)
        #screen.blit(self.m2, self.m2_rect)
        #screen.blit(self.m3, self.m3_rect)
        #screen.blit(self.m4, self.m4_rect)
        a = self.shop_button.render(self.mouse, why_screen[0]) 
        #
        #screen.blit(self.surf_black2, self.shar2_rect )
        #screen.blit(self.surf_black3, self.shar3_rect )
        #screen.blit(self.surf_black4, self.shar4_rect )
        #screen.blit(self.ok_change, self.ok_change_rect)
        print(a)
        if a == 'menu':
            print(5)
            screen_menu.repit()
            self.shop_screen.who_shar = self.shar1.give_nomber()
            self.shars[0] = self.shar1.give_nomber()
            self.shop_screen.mo = self.qu.clik_class.m0
            self.shop_screen.r = self.qu.clik_class.r
            self.shop_screen.maxh = self.qu.clik_class.maxh
        why_screen[0] = a
        #screen.blit(self.fon,(0,0))
def game_screen_control(i):
    if why_screen[0] == "menu":
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running[0] = False  
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    screen_menu.mouse = i.pos 
        screen.fill((0, 0, 0))
        screen_menu.render()
        
    elif why_screen[0] == "start_game":
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running[0] = False 
            if i.type == pygame.MOUSEBUTTONDOWN:
                shop_screen.get_click(i.pos)  
                shop_screen.down_button = True
                #sleep(0.1)
            elif i.type == pygame.MOUSEBUTTONUP:
                #print('---------------------------------------------------------------')
                shop_screen.down_button = '1'
                #sleep(0.2)
            if shop_screen.down_button:
                shop_screen.mouse_coord = i.pos
        screen.fill((0, 0, 0))
        shop_screen.render()
        
    elif why_screen[0] == "game":
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running[0] = False 
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_DOWN:
                    osn_play.key_down = True
                elif i.key == pygame.K_UP:
                    osn_play.key_up = True
                elif i.key == pygame.K_SPACE:
                    if osn_play.peremeshenie_fon == 0:
                        osn_play.extremums = osn_play.extremums_sp
                        osn_play.peremeshenie_fon = 3
                        osn_play.now_time = time()
                elif i.key == pygame.K_HOME:
                    #print('8888888888888888888888888888')
                    why_screen[0] = "start_game"
                    shop_screen.repit_function()
                elif str(i.key) == '13':
                    osn_play.fast_rise = True
                    #print('--------------------------------')
          
            elif i.type == pygame.KEYUP:
                if i.key == pygame.K_DOWN:
                    osn_play.key_down = False
                elif i.key == pygame.K_UP:
                    osn_play.key_up = False 

            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    osn_play.get_click(i.pos) 
                    #sleep(0.4)
                elif i.button == 4:
                    osn_play.plus()
                elif i.button == 5:
                    osn_play.minus() 
                elif i.button == 3:
                    Sputnics(sputnics)
        #screen_menu.render()            
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
    shars = [1,'-']
if shars[0] not in range(1,5):
    shars[0] = 1
pygame.init()
screen = pygame.display.set_mode((1000,600))
fon_start = pygame.image.load("1/login_fon.png").convert()
screen.blit(fon_start, (0,0))
pygame.display.flip()
screen_menu = Menu()
extremums = [(0,0)]
extremums_sp = [(0,0)]
time_max = 0
max_h = 0
sputnics = pygame.sprite.Group()
missiles = pygame.sprite.Group()
prticles = pygame.sprite.Group()
for i in range(choice(range(8,16))):
    Sputnics(sputnics)
sputnics.sprites()[0].create_group_parts(prticles)

why_screen = ['menu',-1720, 490]
osn_play = PlayClass(max_h,time_max, extremums,extremums_sp, fps,coins, sputnics,missiles,prticles, who_shar=shars[0])
shop_screen = MissileShop(osn_play, 60, extremums,who_shar=shars[0])
shop_shar = ShopShar(shars, osn_play, shop_screen)
running = [True]
print(shars)
clock = pygame.time.Clock()
while running[0]:   
    game_screen_control(0)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
f = open("1/coins.txt", "w")
f.write(str(osn_play.coins))
f.close()
f = open("1/shop.txt", "w")
print(shop_shar.qu.shars,shop_shar.shars, shars)
f.write(str(shop_shar.qu.shars[0]) +'\n' + ''.join(list(set(list(shop_shar.qu.shars[1])))))
f.close()
print()
print(osn_play.extremums)