import atomman as am
import multiprocessing as mp
from functools import partial
import re
import os
import numpy as np

# extract the number of files and name of files
def fileprocess(path):
    filenames = []
    filenum = 0
    for lists in os.listdir(path):
        sub_path = os.path.join(path, lists)
        if os.path.isfile(sub_path):
            filenum = filenum+1
            filenames.append(lists)
    # sort the list according to its dump sequence
    filenames.sort(key=lambda x: int(re.findall(r"\d+",x)[0]))

    return filenum, filenames

def ave_atom_pos_write(file_paths, path):
    file_num = len(file_paths)
    atompos = 0
    for i in range(file_num):
        aim_path = os.path.join(path, file_paths[i])
        atompos += am.load('atom_dump', aim_path).atoms.pos
    atompos /= file_num
    
    # read box
    config = am.load('atom_dump', aim_path)
    box = [[config.box.origin[0], config.box.origin[0]+config.box.avect[0]],
           [config.box.origin[1], config.box.origin[1]+config.box.bvect[1]],
           [config.box.origin[2], config.box.origin[2]+config.box.cvect[2]]]
    natoms = config.atoms.natoms
    atom_type = config.atoms.atype
    
    # pbc
    atompos = pbc_wrap_orthogonal(atompos, box)
    
    # repeat z 3 times for nye tensor plot
    repeat_time = 1
    repeat_unit = box[2][1] - box[2][0]
    new_zhi = box[2][0] + repeat_unit * repeat_time
    box = [[box[0][0], box[0][1]],
               [box[1][0], box[1][1]],
               [box[2][0], new_zhi]]
    new_coor = []
    new_type = []
    shift = np.array([0,0,repeat_unit])
    for j in range(repeat_time):
        new_coor = np.append(new_coor, np.array(atompos) + shift*j)
        new_type = np.append(new_type, atom_type)
    atompos = new_coor.reshape((natoms*repeat_time,3))
    atom_type = new_type.reshape((natoms*repeat_time,1))
    natoms *= repeat_time

    # write ave_data_file
    ave_file_path = os.path.join(path, 'ave_file')
    if not os.path.exists(ave_file_path):
        os.makedirs(ave_file_path)
    file_name = file_paths[i]+ '_ave.dat'
    file_path_name = os.path.join(ave_file_path, file_name)
    file = open(file_path_name,'w')
    
    file.write(f"\n\n"
               f"{natoms} atoms\n"
               f"1 atom types\n"
               f"{box[0][0]:>14.12f} {box[0][1]:>14.12f} xlo xhi\n"
               f"{box[1][0]:>14.12f} {box[1][1]:>14.12f} ylo yhi\n"
               f"{box[2][0]:>14.12f} {box[2][1]:>14.12f} zlo zhi\n\n")
    file.write("Atoms\n\n")
    for i in range(natoms):
        file.write(f"{i+1:>8d} {int(atom_type[i]):>4d} \
                   {atompos[i,0]:>14.12f} {atompos[i,1]:>14.12f} {atompos[i,2]:>14.12f}\n")
    file.close()

def pbc_wrap_orthogonal(atom_coor, box_boundary):
    '''
    the box is orthogonal
    '''

    # size of box (Angstrom)
    box_size = [box_boundary[0][1] - box_boundary[0][0],
                box_boundary[1][1] - box_boundary[1][0],
                box_boundary[2][1] - box_boundary[2][0]]

    axis = 2
    for i in range(1,5):
        tempt = atom_coor[:, axis]
        tempt[np.where(tempt > box_boundary[axis][1])] -= box_size[axis]
        tempt[np.where(tempt < box_boundary[axis][0])] += box_size[axis]
        atom_coor[:, axis] = tempt

    return atom_coor

  
def multicore(path, file_set):
    pool = mp.Pool()
    par_ave = partial(ave_atom_pos_write, path = path)
    pool.map(par_ave, file_set)


if __name__ =='__main__':
    #filenum, filename = fileprocess('/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/2_ave_pos/dump_file')
    #path = '/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/2_ave_pos/dump_file'
    #filenum, filename = fileprocess('/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/ave_pos_long_time/dump_file')
    #path = '/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/ave_pos_long_time/dump_file'
    filenum, filename = fileprocess('/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/Ave/Ti/Ti_screw_pyrII_ac_size_55_75_1/dump_file')
    path = '/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/Ave/Ti/Ti_screw_pyrII_ac_size_55_75_1/dump_file'
    

    file_set = []
    ave_file_num = 1000
    frame_interval = 20
    for i in range((filenum-ave_file_num)//frame_interval):
        rep = frame_interval*i
        file_paths = filename[0+rep:ave_file_num+rep]
        file_set.append(file_paths)
    multicore(path, file_set) 
    #'''
    '''
    rep = 0
    file_paths = filename[0+rep:10+rep]
    ave_atom_pos_write(path, file_paths) 
    '''
