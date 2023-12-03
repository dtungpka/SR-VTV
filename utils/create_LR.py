
#First, rename all folder in the src folder to src1, src2,...,srcn and save the name of old folder in a txt file as follows:
#old1 => src1
#old2 => src2
#...

#Second, create a new folder named dst, and create 3 sub folder in dst, named train, test, val
#transverse the src folder, note all the img file
#save in 3 folder, train, test, val in dst folder, in each folder is a LR sub folder
#save the img in the LR folder

import os
import cv2
import shutil
from zipfile import ZipFile 
from tqdm import tqdm
def renames(src):
    #rename all folder in the src folder to src1, src2,...,srcn
    #and save the name of old folder in a txt file
    #old1 => src1
    #old2 => src2
    #...
    #if the folder name is already src1, src2,...,srcn, do nothing
    if os.path.exists('oldname.txt'):
        return
    i = 0
    with open('oldname.txt', 'w',encoding='utf-8') as f:
        for root, dirs, files in os.walk(src):
            for dir in dirs:
                i += 1
                os.rename(os.path.join(root, dir), os.path.join(root, 'src' + str(i)))
                f.write('src' + str(i) + ' <= '+ dir + '\n')
    f.close()
def create_HR(img_path, dst,out_name):
    #TODO
    #Upscaling to X2, X3, X4
    Interpolations = {
        #'INTER_NEAREST': cv2.INTER_NEAREST,
        'INTER_LINEAR': cv2.INTER_LINEAR,
        #'INTER_AREA': cv2.INTER_AREA,
        'INTER_CUBIC': cv2.INTER_CUBIC,
        #'INTER_LANCZOS4': cv2.INTER_LANCZOS4,
        'INTER_LINEAR_EXACT': cv2.INTER_LINEAR_EXACT,
    }
    for upscaler in [4]:
        for interpolation in Interpolations:
            #check if file is already exist
            if os.path.exists(os.path.join(dst, f'HR_X{upscaler}_{interpolation}', out_name)):
                continue

            #check if path exists
            os.makedirs(os.path.join(dst, f'HR_X{upscaler}_{interpolation}'), exist_ok=True)
            #read the img
            img = cv2.imread(img_path)
            #upscale the img
            img = cv2.resize(img, (int(img.shape[1] * upscaler), int(img.shape[0] * upscaler)), interpolation=Interpolations[interpolation])
            cv2.imwrite(os.path.join(dst, f'HR_X{upscaler}_{interpolation}', out_name), img)
            #cv2.imwrite(os.path.join(train_path, 'LR', srcname + '_' + imgname), img)
            #shutil.copy(img, os.path.join(train_path, 'LR', srcname + '_' + imgname))

    

def create_LR(src, dst, scale,splitsize):
    #create a new folder named dst, and create 3 sub folder in dst, named train, test, val
    #transverse the src folder, note all the img file
    #save in 3 folder, train, test, val in dst folder, in each folder is a LR sub folder
    #save the img in the LR folder
    train_path = os.path.join(dst, 'train')
    test_path = os.path.join(dst, 'test')
    val_path = os.path.join(dst, 'val')
    if not os.path.exists(train_path):
        os.makedirs(train_path)
    if not os.path.exists(test_path):
        os.makedirs(test_path)
    if not os.path.exists(val_path):
        os.makedirs(val_path)
    imgs = []
    for root, dirs, files in os.walk(src):
        #save full path of all img file in imgs
        for file in files:
            imgs.append(os.path.join(root, file))
    #split imgs into 3 parts, train, test, val; split size is (.8, .1, .1)
    train_num = int(len(imgs) * splitsize[0])
    test_num = int(len(imgs) * splitsize[1])
    val_num = len(imgs) - train_num - test_num
    train_imgs = imgs[:train_num]
    test_imgs = imgs[train_num:train_num + test_num]
    val_imgs = imgs[train_num + test_num:]
    #save train imgs, with name: src[n]_[imgname].png
    print(f"Processing {len(train_imgs)} train images...")
    for img in tqdm(train_imgs):
        imgname = img.split('/')[-1]
        srcname = img.split('/')[-2]
        #img = cv2.imread(img)
        #img = cv2.resize(img, (int(img.shape[1] / scale), int(img.shape[0] / scale)), interpolation=cv2.INTER_CUBIC)
        #copy img to train folder using shutil
        #if dest img is already exist, skip it
        if os.path.exists(os.path.join(train_path, 'LR', srcname + '_' + imgname)):
            continue
        #check if path exists
        os.makedirs(os.path.join(train_path, 'LR'), exist_ok=True)
        #cv2.imwrite(os.path.join(train_path, 'LR', srcname + '_' + imgname), img)
        shutil.copy(img, os.path.join(train_path, 'LR', srcname + '_' + imgname))
        create_HR(img, train_path,srcname + '_' + imgname)
        
    #save test imgs, with name: src[n]_[imgname].png
    print(f"Processing {len(test_imgs)} test images...")
    for img in tqdm(test_imgs):
        imgname = img.split('/')[-1]
        srcname = img.split('/')[-2]
        #img = cv2.imread(img)
        #img = cv2.resize(img, (int(img.shape[1] / scale), int(img.shape[0] / scale)), interpolation=cv2.INTER_CUBIC)
        #copy img to test folder using shutil
        if os.path.exists(os.path.join(test_path, 'LR', srcname + '_' + imgname)):
            continue
        #check if path exists
        os.makedirs(os.path.join(test_path, 'LR'), exist_ok=True)
        #cv2.imwrite(os.path.join(test_path, 'LR', srcname + '_' + imgname), img)
        shutil.copy(img, os.path.join(test_path, 'LR', srcname + '_' + imgname))
        create_HR(img, test_path,srcname + '_' + imgname)

    #save val imgs, with name: src[n]_[imgname].png
    print(f"Processing {len(val_imgs)} val images...")
    for img in tqdm(val_imgs):
        imgname = img.split('/')[-1]
        srcname = img.split('/')[-2]
        #img = cv2.imread(img)
        #img = cv2.resize(img, (int(img.shape[1] / scale), int(img.shape[0] / scale)), interpolation=cv2.INTER_CUBIC)
        #copy img to val folder using shutil
        if os.path.exists(os.path.join(val_path, 'LR', srcname + '_' + imgname)):
            continue
        #check if path exists
        os.makedirs(os.path.join(val_path, 'LR'), exist_ok=True)
        #cv2.imwrite(os.path.join(val_path, 'LR', srcname + '_' + imgname), img)
        shutil.copy(img, os.path.join(val_path, 'LR', srcname + '_' + imgname))
        create_HR(img, val_path,srcname + '_' + imgname)
def create_DATA(src, dst):
    #create a new folder named dst, and create 3 sub folder in dst, named train, test, val
    #transverse the src folder, note all the img file
    #save in 3 folder, train, test, val in dst folder, in each folder is a LR sub folder
    #save the img in the LR folder
    out_path = os.path.join(dst)
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    
    imgs = []
    for root, dirs, files in os.walk(src):
        #save full path of all img file in imgs
        for file in files:
            imgs.append(os.path.join(root, file))
    print(f"Processing {len(imgs)} images...")
    for img in tqdm(imgs):
        imgname = img.split('/')[-1]
        srcname = img.split('/')[-2]
        #img = cv2.imread(img)
        #img = cv2.resize(img, (int(img.shape[1] / scale), int(img.shape[0] / scale)), interpolation=cv2.INTER_CUBIC)
        #copy img to train folder using shutil
        #if dest img is already exist, skip it
        if os.path.exists(os.path.join(out_path, 'LR', srcname + '_' + imgname[:-4] + '.png')):
            continue
        #check if path exists
        os.makedirs(os.path.join(out_path, 'LR'), exist_ok=True)
        #cv2.imwrite(os.path.join(train_path, 'LR', srcname + '_' + imgname), img)
        lr_img = cv2.imread(img)
        #save as png
        cv2.imwrite(os.path.join(out_path, 'LR', srcname + '_' + imgname[:-4] + '.png'), lr_img)
        create_HR(img, out_path,srcname + '_' + imgname[:-4] + '.png')
        
def unzip_src(src):
    #for all zip file in src, unzip it in [zip_name] folder and delete the zip file
    for root, dirs, files in os.walk(src):
        for file in files:
            if file.endswith('.zip'):
                zip_file = os.path.join(root, file)
                with ZipFile(zip_file, 'r') as zip:
                    zip.extractall(os.path.join(root, file[:-4]))
                os.remove(zip_file)
                print('unzip ' + zip_file + ' to ' + os.path.join(root, file[:-4]))
if __name__ == '__main__':
    src = '/work/21010294/VSR/VTV-Data/frame_anh'
    unzip_src(src)
    renames(src)
    #create_LR(src, '/work/21010294/VSR/VTV-Data/Ver3', 4,(0.8,0.1,0.1))
    #read from command line

    create_DATA(src, '/work/21010294/VSR/VTV-Data/Ver4')

            




