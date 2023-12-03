#tranverse all img in a folder,subfolder,subsubfolder... and convert them from jpg to png

import os
from PIL import Image
from tqdm import tqdm
import sys
def convert(src):
    #get all files in src
    src_files = []
    for root, dirs, files in os.walk(src):
        for file in files:
            #append full path
            src_files.append(os.path.join(root, file))
    #convert each file in src
    pbar = tqdm(src_files)
    for file in pbar:
        if file.split('.')[-1] == 'jpg':
            im = Image.open(file)
            im.save(file.replace('.jpg','.png'))
            #pbar.set_description(file.split('/')[-1] +' => ' +file.replace('.jpg','.png').split('/')[-1])
            #print('converting ' + file + ' to ' + file.replace('.jpg','.png'))
            os.remove(file)
            

if __name__ == '__main__':
    print('Converting...')
    #convert('/work/21010294/VSR/VTV-Data/Ver3/test/LR')
    #convert('/work/21010294/VSR/VTV-Data/Ver3/test/HR_X4_INTER_LINEAR_EXACT')
    #convert('/work/21010294/VSR/VTV-Data/Ver3/test/HR_X4_INTER_CUBIC')
    #convert('/work/21010294/VSR/VTV-Data/Ver3/test/HR_X4_INTER_LINEAR')

    #read from command line
    convert(sys.argv[1])
    print('Done!')