import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import os
import multiprocessing as mp
from scipy.optimize import fminbound

def rotate_strandar_deviation_min(info):
    x = np.array(info['x0'])
    y = np.array(info['y0'])
    x0 = 0
    y0 = 0
    ave_num=20
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
    v_theta = np.array(v_theta)[int(ave_num/2)+1:-int(ave_num/2)] 
    degrees = np.degrees(v_theta)
    Num = degrees.shape[0]
    degree_xaxis = np.linspace(5/1000, (5+100*Num)/1000, Num)
    
    xx = np.array(info['xx'])
    yy = np.array(info['yy'])
    xy = np.array(info['xy'])
    rotate_theta = []
    '''
    for i in range(xx.shape[0]):
        def f(theta):
            return np.cos(theta)*(xy[i]*np.cos(theta)-yy[i]*np.sin(theta))+np.sin(theta)*(xx[i]*np.cos(theta)-xy[i]*np.sin(theta))
        min = fminbound(f, 0, np.pi/2)
        rotate_theta.append(np.degrees(min))
    '''
    for i in range(xx.shape[0]):
        matrix = np.array([[xx[i],xy[i]],[xy[i],yy[i]]])
        values, vectors = np.linalg.eig(matrix)
        maxvalue_index = np.argmax(values)
        vector = abs(vectors[maxvalue_index])
        angle = np.arctan2(vector[1],vector[0])
        rotate_theta.append(np.degrees(angle))
    
    num = xx.shape[0]

    figsize = [150,20]
    fig = plt.figure(figsize=figsize,dpi=72)
    ax1 = fig.add_subplot(111)
    ax = plt.gca()
    x_major_locator=MultipleLocator(10) # every 10 steps shows the label
    y_major_locator=MultipleLocator(30)
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.ylabel('Angle (degree)', fontsize = figsize[0]*0.5)
    plt.xlabel('Time (ns)', fontsize = figsize[0]*0.5)
    plt.xticks(fontsize=figsize[0]*0.5)
    plt.yticks([0,30,42.3799,60,90], ['0 (basal)', 30,'42.4 (PyrI)', 60, '90 (prism)'], fontsize=figsize[0]*0.5)
    plt.axhline(y=42.3799, color='lightgrey', linestyle='-', linewidth=40)
    plt.axhline(y=0, color='lightgrey', linestyle='-', linewidth=40)
    plt.axhline(y=90, color='lightgrey', linestyle='-', linewidth=40)

    xaxis = np.linspace(5/1000, (5+100*num)/1000, num)
    ax1.plot(xaxis, rotate_theta, 'bo-', label='Spreading direction')
    ax1.plot(degree_xaxis, degrees, 'ro-', label='Moving direction')
    plt.legend(fontsize=40,loc=1)
    plt.show()


if __name__ == '__main__':
    info = pd.read_csv('analysis_raw.txt', delim_whitespace = True).sort_values(by='id')
    rotate_strandar_deviation_min(info)
