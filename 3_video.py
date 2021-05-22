import imageio
import os
import re
import cv2

def fileprocess(path):
    filenames = []
    filenum = 0
    for lists in os.listdir(path):
        sub_path = os.path.join(path, lists)
        if os.path.isfile(sub_path) and 'txt' not in sub_path:
            filenum = filenum+1
            new_path = os.path.join(path, lists)
            filenames.append(new_path)
    # sort the list according to its dump sequence
    #filenames.sort(key=lambda x: int(x.split('dump.actuatll_')[-1][:-12]))
    filenames.sort(key=lambda x: int(x.split('fig3/')[-1][:-4]))
    return filenum, filenames

def video(all_path, output_path, output_name):
    img_paths = all_path
    frames = []
    out = output_path + output_name
    #shape = (cv2.imread(all_path).shape[1],cv2.imread(all_path).shape[0])
    video=cv2.VideoWriter(out,cv2.VideoWriter_fourcc(*'MJPG'),24,(5040,2160))
    #video=cv2.VideoWriter(out,cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),10,(2880,1440))
    for i in all_path:
        img=cv2.imread(str(i))
        #img=cv2.resize(img,(504)) #将图片转换为1280*720
        video.write(img)
    video.release()

if __name__ == '__main__':
    #path = '/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/Ave/Ti/Ti_screw_pyrII_ac_size_55_75_1/dump_file/ave_file/fig'
    #path = '/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/2_ave_pos/ave_file/fig'
    #path = '/gauss12/home/cityu/anwenliu/scratch/dislocation_simulation/ave_pos_long_time/dump_file/ave_file/fig'
    path = '/gauss12/home/cityu/anwenliu/git/ave_atom_pos/fig3'
    filenum, filepaths = fileprocess(path)
    output_name = 'v_vector_part.avi'
    output_path = '/gauss12/home/cityu/anwenliu/scratch/video/'
    video(filepaths, output_path, output_name)


