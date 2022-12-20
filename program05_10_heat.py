
from cmath import exp
from matplotlib import pyplot as plt
import numpy as np
import random  as rm
import math
from statistics import  mean
import xlsxwriter
import codecs, json 
import os

t_end=155.5; MIN_temp=-10.;B_koef = 0.0800;A_koef=12;
alpha=2*10**(-16); #размерный коэффициент пропорциональности 
#между градиентом температуры и силой. 
# ht = 0.5;
difmax = 0.00042;
"""Параметры теплового поля"""
dx=2.5*10**(-5);dtau=10**(-10); TMAX=0.95;L=1.8*10**(-2);
nx=int(L/dx+1);ntau=int(TMAX/dtau+1)
ht=2.5*10**(-10)
heatT=10.0           # Температура нагрева
lamb=0.022 #теплопроводность воздуха
# kur=0.4# lamb*ht/dx**2
kur=ht/dx**2
# z=kur*dx**2
z=math.sqrt(ht/kur)
"""Парамтеры бактерий"""
power = 0.5;M = 4# кол бактерий
massa = 4*10**(-16);radius =0.5*10**(-6);
r1=3.9* 0.5*10**(-6);r2=4* 0.5*10**(-6) #ширина стенок без привязки к значениям
radius_x=20*0.5*10**(-6) # радиус круга 
a = 0. 	# границы
b = nx# / 10 #
time_step=[]
one_bacter=[]
x=0
f='new2_pic_with_sphere_'+str(M)+'_warm_mg'
heat1=0;
heat2=nx//2  
g_const=9.8
try:
    os.mkdir(f)
except FileExistsError:
    print('')

def graph_diagram(t,mass,y):
    fig, ax = plt.subplots()
    line1, = ax.plot(t[:], [x[0] for x in mass], '--', linewidth=2,
                 label='1')   
    line2, = ax.plot(t[:], [x[1] for x in mass], '-.', linewidth=2,
                 label='2')  
    line3, = ax.plot(t[:], [x[2] for x in mass], '-', linewidth=2,
                 label='3')  
    line4, = ax.plot(t[:], [x[3] for x in mass], ':', linewidth=2,
                 label='4')  
    line5, = ax.plot(t[:], [x[4] for x in mass], '-', linewidth=2,
                 label='5')  
    line0, = ax.plot(t[:], y[:], '-', linewidth=1,
                 label='max T')  
    ax.legend(loc='lower right')
    plt.show()
    f_grSumm_png=f+'\grapg_summ.png'
    fig.savefig(f_grSumm_png)
def print_mass_to_txt(mass,mass_t):
    # ff = open(f, 'w')
    b = mass.tolist() # nested lists with same data, indices
    f_txt=f+'\ile.txt'
    json.dump(b, codecs.open(f_txt, 'w', encoding='utf-8'), 
              separators=(',', ':'), sort_keys=True, indent=1) ### this saves the array in .json forma
def use_mass_from_txt():
    f_time_txt=f+'mass.txt'
    obj_text = codecs.open(f_time_txt, 'r', encoding='utf-8').read()
    b_new = json.loads(obj_text)
    mass = np.array(b_new)
    print('kek')
    return mass
def print_value(mass,time):
    f_exl=f+'\hello.xlsx'
    workbook = xlsxwriter.Workbook(f_exl)
    worksheet = workbook.add_worksheet()
    row = 0   
    column = 0 
    for thing in time:
        worksheet.write(row, column,  thing)
        row+=1
    for i in range(len(mass)):
        for j in range(len(mass[i])):
            worksheet.write(i, j+1, mass[i][j] ) 
    workbook.close()      
def draw_polar(a,y2,posPx):
    """Ф-я изображения петли"""
    theta = np.linspace(0, 2*np.pi, len(y2))

    r_pos = [r1,r2]
    fig=plt.figure()
    ax = fig.add_subplot(111, polar=True)
    pc = ax.pcolormesh(theta, r_pos, [y2],cmap='hot',
                       vmin = MIN_temp, vmax =-MIN_temp)    
    fig.colorbar(pc, label='Thermal Field')
    # posPx=np.random.uniform(a,b-2,M)
    pos_r = np.full(len(posPx),mean(r_pos)) # позиция круга по радиусу
    theta_1=[2*np.pi/(nx*dx)*thing for thing in posPx]# ПРОВЕРКА np.argmax(y2)=360 -горячая точка
    area =radius_x * pos_r**2 # занимаемая площадь кругом
    colors =['cyan']
    c = ax.scatter(theta_1, pos_r, c=colors, s=area+14, \
                   alpha=0.75)
    plt.title('Time step = '+str(round(a,3)))
    f_fig_polat=f+'\ptime_step_'+str(round(a,3))+'.png'
    # fig.savefig(f_fig_polat)#pic_with_sphere_1_other3_warm
    # plt.show()
    # ax.cla()
    plt.close('all')    
def heat_mass(w):
    """Распределения тепла в петле"""
    wn=np.zeros(len(w))
    for i in range(len(w)):
        try:
            w1_=w[i-1]
        except IndexError:
            w1_=w[nx-1] 
        try:
            w1=w[i+1]
        except IndexError:
            w1=w[0]
        wn[i]=kur*w1_+(1-2*kur)*w[i]+w1*kur
    
        print(wn[i],w[i]*ht,kur*w1_,
              (1-2*kur)*w[i],w1*kur)
    wn[heat1:heat2]=w[heat1:heat2]
    print(wn)
    return wn
def heatFinder(arr,warm):
    """Вычисление координат движения 
    бактерий по тепловому петле"""
    Inew_array=[] 
    maxWarm=0
    ss=[]
    for i in arr:
        gof=0.0 
        Inew=i
        # print(Inew)
        try:
            maxWarm_=warm[Inew]
        except IndexError:
            if Inew==nx:
                Inew=0
                maxWarm_=warm[Inew]
        try: 
            maxWarm_1=warm[Inew-1]
        except IndexError:
            maxWarm_1=warm[-1]
        try: 
            maxWarm_2=warm[Inew-2]
        except IndexError:
            if Inew-2==-1:
                maxWarm_2=warm[-1]
            if Inew-2==-2:
                maxWarm_2=warm[-2]
        try: 
            maxWarm__1=warm[Inew+1]        
        except IndexError:
            maxWarm__1=warm[0]
        try: 
            maxWarm__2=warm[Inew+2]
        except IndexError:
            if Inew+2==nx:
                maxWarm__2=warm[0]
            if Inew+2==nx+1:
                maxWarm__2=warm[1]
        list=[maxWarm_1,maxWarm__1,maxWarm_2,maxWarm__2,maxWarm_]
        maxWarm=mean(list)
        sign=-1
  
        try:
            if  maxWarm<warm[Inew-1] or maxWarm<warm[Inew-2] :
                sign=0 
                
        except IndexError: 
            if Inew-1==-1: 
                if maxWarm<warm[-1]:
                    sign=0
                      
            if Inew-2==-1: 
                if maxWarm<warm[-2]:
                    sign=0
                    
            elif Inew-2==-2:
                if maxWarm<warm[-3]:
                    sign=0
                    
        try:
            if  maxWarm<warm[Inew+1] or maxWarm<warm[Inew+2]:
                sign=1
                
                
        except IndexError:     
            if Inew+1==nx: 
                if maxWarm<warm[0]:
                    sign=1
                    
            if Inew+2==nx: 
                if maxWarm<warm[0]:
                    sign=1
                    
            elif Inew+2==nx+1:
                if maxWarm<warm[1]:
                    sign=1
                    
        Inew_array.append(Inew)
        ss.append(sign)
    return Inew_array, ss
def force(mass_pos):
    """Сила отталкивания"""
    F1=np.zeros(M)
    for i in range(M):
        summaFx=0
        for j in range(M):                
            if i!=j:
                q=mass_pos[i]-mass_pos[j] 
                if abs(q)>(nx-1)*dx//2:
                    if q>0:
                        q=(nx-1)*dx-mass_pos[i]+mass_pos[j]
                    elif q<0:
                        q=(nx-1)*dx+mass_pos[i]-mass_pos[j]
                Sred=abs(q)
                e=math.exp((2*radius-Sred)/0.00008)#B_koef=0.08
                ex=e*q/Sred
                summaFx=summaFx+10*ex#A_koef=12
        F1[i]=summaFx 
    return F1
def force_mg(Im,g):
    Fg=np.zeros(M)
    # print(Im)
    # print(mass_pos)
    # print(g)
    # print(g[nx//2])
    # print(g[0])
    for i in range(M):
        Fg[i]=massa*g[Im[i]]*g_const
        # print("наш голубчик",g[Im[i]])
    return Fg
def real_to_disc(mass_pos,warm):
    """Перенос реальных коорд ш. в дисктретн форму"""
    Im_array=[];aP=[]
    for i in range(M):
        Im = round( mass_pos[i]/dx)
        if Im>=nx-1:
            Im=0
        elif Im<0:
            Im=nx-1        
        Im_array.append(Im)
        aP.append(warm[Im])
    return Im_array,aP
def movi_mass_pos(mass_pos,new_mass_pos,F1,mg,s):
    print('\t\t\t\t\t\t'+str(mass_pos))
    s_mg=np.zeros(M)
    """Уравнение движения"""
    for i in range(M):
        m=mass_pos[i]
        # print((nx-1)//4, (nx-1)-(nx-1)//4)
        if m<=(nx-1)//4 or m>=(nx-1)-(nx-1)//4:
            s_mg[i]=-1 
        else:
            s_mg[i]=1                    
        
        new_mass_pos[i]=m+ht*(F1[i]+mg[i]*s_mg[i]+
                              alpha*np.heaviside(s[i],-1))/massa   
        if new_mass_pos[i]<0:
            new_mass_pos[i]=(nx-1)*dx-abs(new_mass_pos[i])
        if new_mass_pos[i]>(nx-1)*dx:
            new_mass_pos[i]=-(nx-1)*dx+new_mass_pos[i]    
    print(ht*F1[:]/massa  )
    print(ht*mg[:]*s_mg[:]/massa  )
    print(ht*alpha*np.heaviside(s[:],-1)/massa  )
    print(new_mass_pos)
    return new_mass_pos 
def initiat():
    # posPx=[110.]
    posPx=np.random.uniform(0,L,M)
   
    posNx = np.zeros(len(posPx));
    k=posPx
    rw=[]    
    one_bacter.append([rw])
    mass=np.full(M,massa) 
     
    #Задание сеточных координат
    X=[nx*i for i in range(M)]
    x=np.linspace(0,2*np.pi, nx)

    g_cos=abs(np.cos(x))
    # print(g_cos)
    flag=0
    if flag==1:
        warm=use_mass_from_txt()
    else:
        """Обнуление теплового поля"""
        warm=np.full(nx,MIN_temp)

        warm[heat1:heat2]=10 #точка нагрева в петле
        # heat1=0;
        # heat2=nx    #Интервал подогрева
        # warm[heat1:heat2]=10*np.cos(x) #точка нагрева в петле
       
        print(np.argmax(warm),'ИНДЕКС МАКСИМАЛЬНАЯ ТЕМПЕРАТУРА')
    warmN=np.zeros(len(warm))   
    t=0;aPp=[];at=[];aWarm=[]
    n_t=1
    while (t<t_end) :   
        ke=0
        Im_array, aP=real_to_disc(posPx,warm)            
        at.append(t)
        aPp.append(aP)
        warmN=heat_mass(warm)
        # print(warmN)

        aWarm.append(max(warm)) 
        F1=force(posPx)
        mg=force_mg(Im_array,g_cos)
        # print(mg)
        Inew_array, s= heatFinder(Im_array,warm)
        row=[]       
        posNx=movi_mass_pos(posPx,posNx,F1,mg,s)   
        row.append(posPx)
        one_bacter.append([row])        
        # x=x+1
        # draw_polar(t*10**(8),warm,posNx)
        # print(t)
        # print(t*10**(9))
        if ke%500==0:   
            # print('kek')         
            draw_polar(t*10**(9),warm,posPx)
        time_step.append(t)
        warm=warmN
        ke+=1
        t+=ht
        posPx=posNx
        warm=warmN
    # draw_polar(t,warm,posNx)    
    return  t,aPp,at,aWarm, warm

t,aPp,at,aWarm,warm=initiat() 
print_value(aPp,at) 
# print(at)
print_mass_to_txt(warm,at)
graph_diagram(at,aPp,aWarm)


