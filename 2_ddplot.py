from copy import deepcopy
import re
import datetime
import numpy as np
import matplotlib.pyplot as plt
import atomman as am
import os
import atomman.unitconvert as uc
import multiprocessing as mp
from functools import partial



def fileprocess(path):
    filenames = []
    filenum = 0
    for lists in os.listdir(path):
        sub_path = os.path.join(path, lists)
        if os.path.isfile(sub_path):
            filenum = filenum+1
            new_path = os.path.join(path, lists)
            filenames.append(new_path)
    # sort the list according to its dump sequence
    filenames.sort(key=lambda x: int(x.split('dump.actuatll_')[-1][:-8]))
    return filenum, filenames

def plot_and_save(disl_path, base_path, all_path, write_analysis=True):
    base_system = am.load('atom_data',base_path)
    disl_system = am.load('atom_data',disl_path)
    
    #base_system = am.load('atom_data','Ti_screw_basal_a/B_config_disl/nye_per_ref.dat')
    #disl_system = am.load('atom_data','Ti_screw_basal_a/B_config_disl/nye_dislo.dat')
    
    base_system.pbc=(False,False,True)
    disl_system.pbc=(False,False,True)
    
    
    #alat = uc.set_in_units(4.0, 'Å')
    alat = uc.set_in_units(2.93749682368896, 'Å')
    cut_index = 1.3
    neighbors = base_system.neighborlist(cutoff = cut_index*alat)
    dd = am.defect.DifferentialDisplacement(base_system, disl_system, neighbors=neighbors, reference=0)
    
    ddmax = 2.94749682368896/2   # a/2<110> fcc dislocations use |b|/4
    

    # Set dict of keyword parameter values (just to make settings same for all plots below)
    params = {}
    params['plotxaxis'] = 'x'
    params['plotyaxis'] = 'y'
    params['xlim'] = (-20,20)
    params['ylim'] = (-40,40)
    
    #params['zlim'] = (-0.01, alat*6**0.5 / 2 + 0.01) # Should be one periodic width (plus a small cushion)
    #params['zlim'] = (-0.1,1.5)
    #params['zlim'] = (-0.01, 1.44)
    params['figsize'] = 10         # Only one value as the other is chosen to make plots "regular"
    params['arrowwidth'] = 1/100    # Made bigger to make arrows easier to see
    params['arrowscale'] = 1#2.4     # Typically chosen to make arrows of length ddmax touch the corresponding atom circles
    params['atomcmap'] = 'gray'
    params['figsize'] = 20
    params['alat'] = alat #to dismiss some ddvector if less than 0.1*burers
    
    ####params for nye###
    params['cmap'] = 'bwr'
    params['xbins'] = 200
    params['ybins'] = 200
    params['scale'] = 1
    params['nye_index'] = [2,2]
    
    
    #disl_system.pbc=(True,True,True)
    # Give base and disl systems with a cutoff
    strain = am.defect.Strain(base_system, basesystem=disl_system, cutoff=cut_index*alat, theta_max=10)
    #strain = am.defect.Strain(disl_system, basesystem=base_system, cutoff=1.25*alat) 
    strain.save_to_system()
    straindict = strain.asdict()
    
    #### plot seetings ##
    par={}
    par['fontsize'] =40
    #####
    
    nye = 'Nye'+'['+str(params['nye_index'][0]+1)+','+str(params['nye_index'][1]+1)+']'
    fig = dd.plot(base_system, 'z', ddmax, **params)
    line_index = all_path.index(disl_path)+1
    plt.title(nye+' with DD[3]   ' + f'Time: {line_index//10} ns' ,**par)
    
    # plot time scale:
    #plt.xlabel(f'Time: {line_index//10} ns', fontsize = 35)
    plt.xlabel('x ('+ u'\u212B'+')', fontsize = 45)
    plt.ylabel('y ('+ u'\u212B'+')', fontsize = 45).set_rotation(0)
    
    path, name = os.path.split(disl_path)
    new_path = os.path.join(path,'fig')
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    new_name = name + str('.png')
    new_fig_path = os.path.join(new_path,new_name)
    plt.savefig(new_fig_path)
    
    if write_analysis==True:
        data_path = os.path.join(new_path,'analysis_raw.txt')
        file = open(data_path,'a')
        file.write(f"{line_index:>8d} {fig.x0:>10.8f} {fig.y0:>10.8f} {fig.x_sq:>10.8f} {fig.y_sq:>10.8f} {fig.xy:>10.8f}\n")
        file.close()
	        


def multicore(disl_path, base_path):
    pool = mp.Pool()
    par_plot = partial(plot_and_save, base_path = base_path, all_path = disl_path)
    pool.map(par_plot, disl_path)

if __name__ == '__main__':
    #path = '/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/2_ave_pos/dump_file'
    path = '/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/ave_pos_long_time/dump_file/ave_file'    
    #path = '/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/Ave/Ti/Ti_screw_pyrII_ac_size_55_75_1/dump_file/ave_file'
    filenum, filepaths = fileprocess(path)
    
    # open a txt for analysis writing
    path, name = os.path.split(filepaths[0])
    #path_dir = os.path.join(path,'fig')
    #if not os.path.exists(path_dir):
     #   os.makedirs(path_dir)
    data_path = os.path.join(path,'fig/analysis_raw.txt')
    file = open(data_path,'w')
    file.write(f"id x0 y0 xx yy xy\n")
    file.close()
    
    #base_path = '/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/Ave/Ti/Ti_screw_pyrII_ac_size_55_75_1/Ti_screw_pyrII_ac_perfect_reference.dat'
    base_path = '/gauss12/home/cityu/anwenliu/git/dd/input/300K_ave_Ti_screw_a/5000/nye_per_ref.dat'
    disl_path = filepaths 
    multicore(disl_path, base_path)

    '''
    disl_path = '/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/2_ave_pos/ave_file/dump.actuatll_7600_ave.dat'
    plot_and_save(disl_path, base_path)
    '''




































