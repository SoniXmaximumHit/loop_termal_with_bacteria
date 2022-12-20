#Решение задачи активного контроля тепловой конвекцией 
# в тороидальном вертикальном контуре, 
# нагреваемом снизу и охлаждаемом сверху.

# 20.	Singer J., Bau H. H. 
# Active control of convection //
# Physics of Fluids A: Fluid Dynamics. – 1991. – 
# Т. 3. – №. 12. – С. 2859-2865.

# Singer J., Wang Y. Z., Bau H. H. 
# Controlling a chaotic system //
# Physical Review Letters. – 1991. – 
# Т. 66. – №. 9. – С. 1123.

from cmath import exp
from matplotlib import pyplot as plt
import numpy as np
import random  as rm
import math
import xlsxwriter
import codecs, json 
import os
from lu3 import decLU3, solveLU3
# g - ускорение свободного падения (м/с²)
# betta - коэффициент теплового расширения ((1/K) x 10-3)
# del_term - усредненная разница температур стенки между 
# нижней и верхней частями контура (К)
# D - диаметр тора (м), d - диаметр трубы (м)
# ro0 - средняя плотность жидкости (кг/м3)
# Cp - удельная теплоёмкость (тепловая мощность) (кДж/(кг* K))
# h - коэффициент теплопередачи между жидкостью и стенками трубы ()
# v - кинематеческая вязкость ((м²/с) x 10−6)  
# alpha -  температуропроводность жидкости (м²/с)
# k - теплопроводимость (Вт/(м* K))
# Pr - число Прандтля, Nu - число Нуссельта
# tau - шкала времени
# P - число Прандтля петли
# Biot - число Био
# d_teta - изменение угла  Тета (O) (радианы)
# n_teta - количество делений петли 
# d_t - изменение времени (с)
# t_end - конечное время (с)
# u -  функция скорость (м/с)
# term -  функция температуры (К)

class Parameter_Solution():
    """Параметры задачи"""
    def __init__(self):     
        self.g = 9.78; self.betta = 3.67*10**(-3); self.del_term = 1.; self.D = 0.760; 
        self.k = 0.0243; self.d = 0.03; self.h = 3.66*self.k/self.d; #Nu=3.66 при пост тепло.потоке
        self.Cp = 1.005; self.v = 13.3*20**(-6); self.alpha = 1.9*10**(-5); 
        self.ro0 = 1.293; self.tau = self.ro0*self.Cp*self.d/(4*self.h);
        self.Nu = self.h*self.d/self.k; self.Pr = self.v/self.alpha; 
        self.P = 8*self.Pr/self.Nu; self.Biot = (self.d/self.D)**2/self.Nu;
        self.Ra = self.g*self.betta*self.del_term*self.tau**2/self.D/self.P; 
        self.d_teta = np.pi*self.D*0.001; 
        self.n_teta = int(np.pi*self.D/self.d_teta + 1); 
        # self.n_teta =10 # Для проверки
        self.teta=np.linspace(0,2*np.pi, self.n_teta);self.t_end=100;
        self.d_t = 0.01; 
        self.n_t = int(self.t_end/self.d_t );
        # self.n_t = 10; # Для проверки
        self.dt_dteta =self.d_t/self.d_teta; 
        self.Wn = np.linspace(1,1,self.n_t); 
        self.W0 = np.linspace(1,1,self.n_t)
        self.Vn = np.linspace(1,1,self.n_t); 
        self.C0 = np.linspace(1,1,self.n_t)
        self.Cn = np.linspace(1,1,self.n_t); 
        self.Sn = np.linspace(1,1,self.n_t)
        self.t = np.linspace(0,self.n_t,self.n_t)

class Heat_Calc(Parameter_Solution):
    def __init__(self):
        """Инициализация параметров задачи"""
        super().__init__()
        
    def term_calc(self,u_past, term_past):
        """Рассчёт теплового поля на j+1 шаге по времени"""
        a=0; b=0;c=0;d=0;d1=0;term_new=np.zeros(len(term_past ))
        for i in range(self.n_teta-1):
            ip1 = i + 1; im1 = i - 1  
            if i ==  self.n_teta-1:
                ip1 = 0                 
            elif i == 0:
                im1 = -1                
            a=(1 + self.dt_dteta*u_past[i] - self.dt_dteta*self.Biot)
            b=(-self.dt_dteta*u_past[i] + self.dt_dteta/2*self.Biot)
            c=(self.dt_dteta/2*self.Biot)
            d1=(self.term_wall1(i) - self.term_fluid1(i,term_past[i]))   
            # d.append(self.term_wall(j) - self.term_fluid(j))                             
            term_new[i] = term_past[i]*a + term_past[ip1]*b\
                + term_past[im1]*c +d1

            
            
        return  term_new
    def term_wall1(self, teta_i):
        """Слагаемое тепл.поля стенки
        Ra1*Td(teta)={Td=1, Пи<teta<2Пи;  
                    Td=0, 0<=teta<=Пи}"""
        Ra1=1.0
        if self.teta[teta_i] > np.pi or self.teta[teta_i] < 2*np.pi:
            term_w = Ra1
        else:
            term_w = 0.
        return term_w
    def term_fluid1(self, teta_i,term_i):
        """Слагаемое тепл.поля жидкости
        T1*h(teta)={h=0, Пи<teta<2Пи;  
                    h=1, 0<=teta<=Пи}"""
        Ra1=1.0
        if self.teta[teta_i] <= np.pi or self.teta[teta_i] >= 0.:
            term_w = term_i
        else:
            term_w = 0.
        return term_w 

    def u_calc(self, u_ji, term_ji):
        """Рассчёт скорости u на j+1 шаге по времени"""
        u_new=[];
        u_i  = u_ji; term_i = term_ji;
        u_j_plus_1=[]  
        sum = self.sum_term(term_i)
        for i in range(self.n_teta):   
            u_j_plus_1.append(u_i[i]*(1 - self.P*self.d_t)+\
                1/np.pi*self.Ra*self.P*sum)
        u=np.asarray(u_j_plus_1)
        return u
    def term_wall(self, t_i):
        """Разл. в ряд Фурье тепл.поля стенки"""
        sum=0
        for i in range(len(self.teta)-1):
            sum+=self.Wn[t_i]*math.sin(self.teta[i]) +\
                self.Vn[t_i]*math.cos(self.teta[i])   
        term_w=self.W0[t_i] + sum        
        return term_w
    def term_fluid(self, t_i):
        """Разл. в ряд Фурье тепл.поля жидкости"""
        sum=0
        for i in range(len(self.teta)-1):
            sum+=self.Sn[t_i]*math.sin(self.teta[i]) +\
                self.Cn[t_i]*math.cos(self.teta[i])
        term_f=self.C0[t_i] + sum
        return term_f   
    def sum_term(self,term_i):
        """Рассчёт температурного интеграла для скорости"""
        sum=0
        n = len(self.teta)
        for i in range(n-2):
            sum+=term_i[i+1]*math.cos(self.teta[i+1])
        sum_0n = (sum+(term_i[0]*math.cos(self.teta[0])+\
            term_i[n-1]*math.cos(self.teta[n-1]))/2)*self.d_teta
        return sum_0n

class Array_in_txt(): 
    """Работа с текстовым файлом"""   
    def __init__(self) -> None:
        self.file='array.txt'
    def print_mass_to_txt(self,f,array, regime='w'):
        """Запись массива в файл"""
        name_file= f+'_'+ self.file  
        # print(type(array) )
        b = array.tolist() # nested lists with same data, indices
        json.dump(b, codecs.open(name_file, regime , encoding='utf-8'), 
                separators=(',', ':'), sort_keys=True, indent=1) ### this saves the array in .json forma
    def use_mass_from_txt(self,f):
        """Чтение массива из файла"""
        name_file=f+'_'+ self.file
        obj_text = codecs.open(name_file, 'r', encoding='utf-8').read()
        print(obj_text)
        b_new = json.loads(obj_text)
        array = np.array(b_new)
        # print('kek')
        return array

class Draw_Polar_Coords(Parameter_Solution):
    """Изображение петли"""
    def __init__(self) -> None:
        super().__init__()  
    def draw(self,teta,u,term):
        """Ф-я изображения петли"""
        r_pos = [self.D - self.d/2 , self.D + self.d/2]
        fig, axarr=plt.subplots(1, 2, figsize=(15, 5), \
            subplot_kw=dict(projection='polar'))
        k0=axarr[0].pcolormesh(teta, r_pos,[u],cmap='hot')
        axarr[0].set_title('Скорость')
        k1= axarr[1].pcolormesh(teta, r_pos,[term],cmap='hot')
        axarr[1].set_title('Температура')

        # fig = plt.figure()
        # axarr[1] = fig.add_subplot(111, polar=True)
        # pc = axarr .pcolormesh(teta, r_pos, [term],cmap='hot',
        #                 vmin = min(term), vmax =max(term))    
        fig.colorbar(k0,ax=axarr[0])
        fig.colorbar(k1,ax=axarr[1])
        # plt.title('Тепловое поле')
        plt.show()
        plt.close('all')   
         
class Creat_array(Parameter_Solution):
    def __init__(self) -> None:
        super().__init__()  
        self.u_Start = np.zeros(self.n_teta)
        self.term_Start = np.zeros(self.n_teta)
        self.term_New = np.zeros(self.n_teta)
        self.u_New=np.zeros(self.n_teta)
    def main(self):
        """Запуск алгоритма решения"""
        hc = Heat_Calc()  
        bp = BuildPlot()
        arr_txt = Array_in_txt()
        dpc=Draw_Polar_Coords()
        self.term_Past =   self.term_Start
        self.u_Past =  self.u_Start
        
        flag = 0
        if flag==0:
            arr_txt.print_mass_to_txt('u', self.term_Past)            
            arr_txt.print_mass_to_txt('term',self.u_Past)
            # dpc.draw(self.teta,self.u_New[:],self.term_New[:])
        elif flag==1:
            self.term_End = arr_txt.use_mass_from_txt('term')
            self.u_End = arr_txt.use_mass_from_txt('u')
            
        for j in range(self.n_t-2):
            """Рассчёт поля скоростей и теплового на j+1 шаге по времени"""
            self.term_New =  hc.term_calc(self.u_Past,self.term_Past) 
            self.u_New = hc.u_calc(self.u_Past,self.term_Past)
            self.u_Past=self.u_New
            self.term_Past=self.u_New
            arr_txt.print_mass_to_txt('u',self.u_New,'a')  
            arr_txt.print_mass_to_txt('term',self.term_New,'a')
        dpc.draw(self.teta,self.u_New[:],self.term_New[:])    


        # bp.draw_diagram(self.teta,self.term_End[-1][:])
        # dpc.draw(self.teta,self.u_End[-1][:],self.term_End[-1][:])

class BuildPlot(Creat_array,Parameter_Solution):
    """Построение диаграммы"""
    def __init__(self) -> None:
        super().__init__()
    def draw_diagram(self,x,y): 
        fig, ax = plt.subplots()  
        line1, = ax.plot(x, y, '--', linewidth=2,
                 label='kek')
        ax.legend(loc='lower right')
        plt.show()
ca=Creat_array()
ca.main()
# u_End, term_End = ca.main()

# for j in range(len(u_End)-1):
#     for i in range(len(u_End[j])-1):
#         print(term_End[j][1])

        