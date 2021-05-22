import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import os
import multiprocessing as mp

def multiplotting(x, y, ave_num=20):
    x0 = 0
    y0 = 0
    for i in range(1,ave_num+1):
        zero = [0]
        new_x = np.insert(x,0,zero*i)
        new_x = np.append(new_x,zero*(ave_num+1-i))
        new_y = np.insert(y,0,zero*i)
        new_y = np.append(new_y,zero*(ave_num+1-i))
        x0 += new_x/ave_num
        y0 += new_y/ave_num
    v_theta =[]
    for i in range(x0.shape[0]):
        if i ==0:
            dx = x0[i+1]-x0[i]
            dy = y0[i+1]-y0[i]
        if i== x0.shape[0]-1:
            dx = x0[i]-x0[i-1]
            dy = y0[i]-y0[i-1]
        else:
            dx = (x0[i+1]-x0[i-1])/2
            dy = (y0[i+1]-y0[i-1])/2
        if dx == 0:
            angle = np.pi/2
        if  dy ==0 :
            angle = 0
        elif dx>0 and dy>0 :
            angle = np.arctan2(dy,dx)
        elif dx>0 and dy<0 :
            angle =  -np.arctan2(dy,dx)
        elif dx<0 and dy<0 :
            angle = np.pi + np.arctan2(dy,dx)
        elif dx<0 and dy>0 :
            angle = np.pi - np.arctan2(dy,dx)
        v_theta.append(angle)
    v_theta = np.array(v_theta)
    #print(len(v_theta),len(x0),len(y0))
    input = []
    for i in range(ave_num, x0.shape[0]-ave_num):
        input.append([x0[ave_num:i+1], y0[ave_num:i+1], v_theta[ave_num:i+1], i-ave_num])
    pool = mp.Pool()
    pool.map(save_image, input)
    
def save_image(info):
    x0 = np.array(info[0])
    y0 = np.array(info[1])
    id = info[3]
    v_theta = info[2]
    num = x0.shape[0]
    
    xaxis = np.linspace(5/1000, (5+5*num)/1000, num)

    figsize = [70,30]
    fig = plt.figure(figsize=figsize,dpi=72)
    ax1 = fig.add_subplot(111)
    middle = xaxis[-1]
    if middle-2<0:
    	xlim = 0
    	xlim_hi = 3
    else:
        xlim = middle-2  
        xlim_hi = middle+1  
    ax1.axis([xlim,xlim_hi,-3,93])
    ax = plt.gca()
    x_major_locator=MultipleLocator(0.5) # every 10 steps shows the label
    y_major_locator=MultipleLocator(30)
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.ylabel('Angle (degree)', fontsize = figsize[0]*2)
    plt.xlabel('Time (ns)', fontsize = figsize[0]*2)
    plt.xticks(fontsize=figsize[0]*1.5)
    plt.yticks([0,30,42.3799,60,90], ['0 (Basal)', 30,'42.4 (Pyr.I)', 60, '90 (Prism.I)'], fontsize=figsize[0]*1.5)
    degrees = np.degrees(v_theta)
    plt.axhline(y=42.3799, color='lightgrey', linestyle='-', linewidth=40)
    plt.axhline(y=0, color='lightgrey', linestyle='-', linewidth=40)
    plt.axhline(y=90, color='lightgrey', linestyle='-', linewidth=40)
    bwith = 1.5
    ax.spines['bottom'].set_linewidth(bwith)
    ax.spines['left'].set_linewidth(bwith)
    ax.spines['top'].set_linewidth(bwith)
    ax.spines['right'].set_linewidth(bwith)

    ax1.plot(xaxis, degrees,'bo-', linewidth=16, markersize=40 )
    path = 'fig3/'+str(id)+'.png'
    plt.subplots_adjust(left=0.2, bottom=0.2)
    plt.savefig(path)
        

def draw_dislocation_position_change(info):
    x = np.array(info['x0'])
    ave_num = 20
    x0 = 0
    y0 = 0
    y = np.array(info['y0'])
    for i in range(1,ave_num+1):
        zero = [0]
        new_x = np.insert(x,0,zero*i)
        new_x = np.append(new_x,zero*(ave_num+1-i))
        new_y = np.insert(y,0,zero*i)
        new_y = np.append(new_y,zero*(ave_num+1-i))
        x0 += new_x/ave_num
        y0 += new_y/ave_num

    v_theta =[]
    DX = []
    DY = []
    for i in range(x0.shape[0]):
        if i ==0:
            dx = x0[i+1]-x0[i]
            dy = y0[i+1]-y0[i]
        if i== x0.shape[0]-1:
            dx = x0[i]-x0[i-1]
            dy = y0[i]-y0[i-1]   
        else:
            dx = (x0[i+1]-x0[i-1])/2
            dy = (y0[i+1]-y0[i-1])/2
        DX.append(dx)
        DY.append(dy)
        if dx == 0:
            angle = np.pi/2
        if  dy ==0 :
            angle = 0
        elif dx>0 and dy>0 :
            angle = np.arctan2(dy,dx)
        elif dx>0 and dy<0 :
            angle =  -np.arctan2(dy,dx)
        elif dx<0 and dy<0 :
            angle = np.pi + np.arctan2(dy,dx)
        elif dx<0 and dy>0 :
            angle = np.pi - np.arctan2(dy,dx)

        v_theta.append(angle)
    num = x0.shape[0]
    xaxis = np.linspace(5/1000, (5+5*num)/1000, num)

    figsize = [140,20]
    fig = plt.figure(figsize=figsize,dpi=72)
    ax1 = fig.add_subplot(111)
    #ax1.axis([-0.5,14,-1,91])
    ax = plt.gca()
    x_major_locator=MultipleLocator(1) # every 10 steps shows the label
    y_major_locator=MultipleLocator(30)
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.ylabel('v vector angle (degree)', fontsize = figsize[0]*0.5)
    plt.xlabel('time (ns)', fontsize = figsize[0]*0.5)
    plt.xticks(fontsize=figsize[0]*0.5)
    plt.yticks([0,30,42.3799,60,90], ['0 (basal)', 30,'42.4 (PyrI)', 60, '90 (prism)'], fontsize=figsize[0]*0.5)
    degrees = np.degrees(v_theta)
    plt.axhline(y=42.3799, color='lightgrey', linestyle='-', linewidth=40)
    plt.axhline(y=0, color='lightgrey', linestyle='-', linewidth=40)
    plt.axhline(y=90, color='lightgrey', linestyle='-', linewidth=40)

    ax1.plot(xaxis, degrees,'o')
    plt.show()



if __name__ == '__main__':
    info = pd.read_csv('analysis_raw.txt', delim_whitespace = True).sort_values(by='id')
    #draw single figure
    #draw_dislocation_position_change(info)
    
    # save set figures
    x0 = np.array(info['x0'])
    y0 = np.array(info['y0'])
    multiplotting(x0, y0, ave_num=20)
    
