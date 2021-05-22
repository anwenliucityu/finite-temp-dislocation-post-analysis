import imageio
import os
import re
import cv2

re_digits = re.compile(r'(\d+)')
def emb_numbers(s):
    pieces=re_digits.split(s)
    pieces[1::2]=map(int,pieces[1::2])    
    return pieces

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
    #filenames.sort(key=lambda x: int(re.findall(r"\d+",x)[0]))
    filenames.sort(key = emb_numbers)

    return filenum, filenames

def compose_gif(all_path):
    img_paths = all_path
    gif_images = []
    for path in img_paths:
        print(path)
        gif_images.append(imageio.imread(path))
    imageio.mimsave("move.gif",gif_images,fps=24)

if __name__ == '__main__':
    #path = '/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/2_ave_pos/ave_file/fig'
    path = '/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/Ave/Ti/Ti_screw_pyrII_ac_size_55_75_1/dump_file/dump_file/ave_file/fig'
    filenum, filepaths = fileprocess(path)
    #print(filepaths)
    compose_gif(filepaths)
