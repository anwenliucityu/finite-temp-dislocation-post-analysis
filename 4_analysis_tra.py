import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import os
import multiprocessing as mp

def draw_dislocation_position_change(info):
    x0 = info['x0']
    y0 = info['y0']
    v_theta =[]
    for i in range(x0.shape[0]-1):
        v_theta.append(np.arctan2((y0[i+1]-y0[i]),(x0[i+1]-x0[i])))
    num = x0.shape[0]
    xaxis = np.linspace(5, 5+5*num, num-1)
    degrees = abs(np.degrees(v_theta))
    plt.plot(xaxis, degrees)
    plt.show()
    
def tra(info):
    figsize = [12,20]
    fig = plt.figure(figsize=figsize,dpi=72)
    plt.xticks(fontsize=figsize[0]*1.5)
    plt.yticks(fontsize=figsize[0]*1.5)

    ax1 = fig.add_subplot(111)
    ax1.axis([-8,13,-30,29])
    x0 = info['x0']
    y0 = info['y0']
    ax1.plot(x0, y0,'.-')
    ax1.set_aspect('equal') 
    ax = plt.gca()
    x_major_locator=MultipleLocator(2) # every 10 steps shows the label
    y_major_locator=MultipleLocator(2)
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.xlabel('x ('+ u'\u212B'+')', fontsize = figsize[0]*2.2)
    plt.ylabel('y ('+ u'\u212B'+')', fontsize = figsize[0]*2.2).set_rotation(0)
    plt.title('Trajectory of defined dislocation line position', fontsize = figsize[0]*2)
    plt.show()


def save_frame_image(x0y0):
    figsize = [12,20]
    fig = plt.figure(figsize=figsize,dpi=72)
    plt.xticks(fontsize=figsize[0]*1.5)
    plt.yticks(fontsize=figsize[0]*1.5)
    x0 = x0y0[0]
    y0 = x0y0[1]
    ax1 = fig.add_subplot(111)
    ax1.axis([-8,13,-30,29])
    ax1.plot(x0, y0,'.-')
    ax1.set_aspect('equal') 
    ax = plt.gca()
    x_major_locator=MultipleLocator(2) # every 10 steps shows the label
    y_major_locator=MultipleLocator(2)
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.xlabel('x ('+ u'\u212B'+')', fontsize = figsize[0]*2.2)
    plt.ylabel('y ('+ u'\u212B'+')', fontsize = figsize[0]*2.2).set_rotation(0)
    plt.title('Trajectory of defined dislocation line position', fontsize = figsize[0]*2)
    #plt.show()
    i = x0.shape[0]
    path = 'fig/'+str(i+1)+'.png'
    plt.savefig(path)






if __name__ == '__main__':
    info = pd.read_csv('analysis_raw.txt', delim_whitespace = True).sort_values(by='id')
    #draw_dislocation_position_change(info)
    x0y0 = []
    for i in range(1,info['x0'].shape[0]+1):
        x0y0.append([info['x0'][:i], info['y0'][:i]])
        #y0.append(info['y0'][:i])
    #x_y = list(zip(x0,y0))
    
    pool = mp.Pool()
    pool.map(save_frame_image, x0y0)
    
    #tra(info)


