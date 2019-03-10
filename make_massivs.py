# -*- coding: utf8 -*-
from math import pi, degrees
from numpy import*
from scipy.integrate import odeint 
import matplotlib.pyplot as plt


def func(mo,r, graph=False):
    g = 9.81  # ускорение свободного падения на земле в м/с2.
    rv = 1.29  # плотность атмосферного воздуха в кг/м3.
    rg = 0.17  # плотность гелия в кг/м3.
    R = r  # радиус оболочки стратостата в м.
    b = 0.000125  # константа, связанная с плотностью воздуха в 1/м
    a = 6.5*10**-3  # константа, связанная с температурой воздуха в К/м
    c = 0.8  # коэффициент лобового сопротивления
    V = (4/3)*pi*R**3
    print(V)
    p2 = 3*c/(8*R)  # введенный параметр
    Vmin=500  # начальный объём шара в/м3.
    c=0.8  #коэффициент лобового сопротивления
    rs=rg+mo/Vmin  # суммарная плотность материала стратостата,
    # массы гелия и нагрузки
    p1=rv/rs  # введенный параметр
    T0 = 300  # температура на уровне моря
    rgu=1.2  # плотность образовавшейся газовой смеси 
    # после  стравливания гелия в кг/м3 
    tz = 900
    vc = [V - 1000]
    
    
    def fun(y, t):  
        y1,y2= y
        if t < tz:
            if y2==0:
                pass
            if y2<=0:
                if kostil_3[0]:
                    kostil_3[0] = False
                pep8 = (g * (rv * V * exp(-b * y1) - mo - rg))
                return [y2,(pep8 + (( rv * c * exp(-b * y1)) / 2) * y2 ** 2)]
            else:
                if not(kostil_3[0]): 
                    kostil_3[0] = True 
                pep8 = (g * (rv * V * exp(-b * y1) - mo - rg))
                return [y2,(pep8 - (( rv * c * exp(-b * y1)) / 2) * y2 ** 2)]
        elif t > tz:
            vc[0] -= 0.063
            if y1 < 0.0:
                return [0,0]
            
            if y2<=0:
                pep8 = (g * (rv * vc[0] * exp(-b * y1) - mo - rgu))
                return [y2, (pep8 + ((rv * c * exp(-b * y1)) / 2) * y2 ** 2)] 
            else:
                pep8 = (g * (rv * vc[0] * exp(-b * y1) - mo - rgu))
                return [y2,(pep8 - ((rv * c * exp(-b * y1)) / 2) * y2 ** 2)]   
            
            
    kostil_3 = [True]
    t = [i/1000 for i in range(tz*1000)]
    y0 = [0,0]
    [y1,y2]=odeint(fun, y0,t, full_output=False).T
    print()
    extremums = [(t[i],round(y1[i],1))
                 for i in range(len(y2[:tz*1000:])) if round(y2[i],0) == 0.0 ]
    extremums = [extremums[i]
                 for i in range(len(extremums))
                 if extremums[i][1] != extremums[i-1][1]]
    y1 = [i for i in y1]
    y2 = [i for i in y2]
    print(t)
    print(*extremums, sep='\n')
    extremums_sp = [(0,0,)]
    max_h_fiying = max(y1)
    time_max_fliting = t[y1.index(max_h_fiying)]
    print("max_h_fiying", max_h_fiying)
    print("time_max_fliting",time_max_fliting)
    with open('mass_'+str(mo)+"_" + str(R) + '.py', 'w') as f:
        f.write('mass = ['  )
        for i in range(len(extremums)):
            pep8 = '\t(' + str(round(extremums[i][0], 2))
            f.write(pep8 + ', ' + str(round(extremums[i][1], 2)) + ')')
            f.flush()
            if i + 1 == len(extremums):
                break
            f.write(', \n')
        f.write(']\nmass_sp = [ ')
        
        for i in range(len(extremums_sp)):
            pep8 = '\t(' + str(round(extremums_sp[i][0], 2))
            f.write(pep8 + ', ' + str(round(extremums_sp[i][1], 2)) + ')')
            f.flush()
            if i + 1 == len(extremums_sp):
                break
            f.write(', \n')
        pep8 = '\ntime_max = '+ str(time_max_fliting)
        f.write( ']\nmax_h = ' + str(max_h_fiying) + pep8)
        f.close()
    
    if graph:
        pep8 = "Подъём, зависание стратостата \n"
        pep8 += "с нежёсткой оболочкой сферической формы  \n"
        pep8 += "Объём: %s м3. Масса : %s кг." %(round(V, 0), mo)
        pep8 += "Подъёмная сила: %s kН. "%round(0.001*g*rv*V,0)
        plt.title(pep8)
        pep8 = 'Максимальная высота подъёма: %s км. \n'%round(max(y1)/1000,2)
        pep8 += "Максимальная скорость: % s м/с.\n"%round(max(y2),2)
        plt.plot(t, y1, label=pep8)        
        plt.ylabel('Высота в м')
        plt.xlabel(' Время в сек.')
        plt.legend(loc='best')
        plt.grid(True)
        print()
        plt.show()      
    extremums = []
    y1, y2, t = [], [], []
    print('mo f', mo)
    
