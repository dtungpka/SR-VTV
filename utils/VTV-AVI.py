import cv2
import numpy as np
import os
from tqdm import tqdm
import time
import argparse

def load_images(images_location):
    Images = {}
    errs = []
    no_vid = 0
    RENAME_LIST = ['_SRFormer_DF2k_X4_VTV2','_vtv_test_n02','_CALGAN-VTV-T4','_SRFormer_DF2k_X4_VTV2']
    for root, dirs, files in os.walk(images_location):
        #print all root, directories, and files in the current directory 
        for file in files:
            #for renaming
            file_ = file
            for rename in RENAME_LIST:
               file_ = file_.replace(rename, '')
            if file_.endswith('.png') and '_cmap' not in file_:
                img_type = root.split('/')[-1]
                #print(f'Found image type: {img_type} from {root}; {file_}')
                video = file_.split('_frame_')[0]
                #add full image path to Images dictionary
                if img_type not in Images:
                    Images[img_type] = {}
                    print(f'Found image type: {img_type} from {root}; {file_}')
                if video not in Images[img_type]:
                    Images[img_type][video] = {}
                    no_vid += 1
                try:
                    #print(f"File name: {file} | {int(file.split('_frame_')[1].split('.png')[0])}")
                    Images[img_type][video][int(file_.split('_frame_')[1].split('.png')[0])] = os.path.join(root, file)
                except Exception as e:
                    errs.append(f'Error: {img_type}/{video}/{file} is not a valid image | {e}')

    print(f"Loaded {len(Images)} image types, {no_vid} videos")
    
    
    for img_type in Images:
        for video in Images[img_type]:
            time.sleep(.1)
            print(f'\rChecking integrity of {img_type}/{video} images... ', end='')
            current_index = 0
            err = 0
            for i in range(len(Images[img_type][video])):
                if current_index not in Images[img_type][video]:
                    errs.append(f'Error: {img_type}/{video}/{current_index} is missing')
                    err += 1
                current_index += 1
            if err == 0:
                print('OK!', end=' '*30)
            else:
                print(f'{err} errors!')
    print((f'\n{len(errs)} errors found:' + '\n'.join(errs)) if len(errs) > 0 else '\nNo errors found')
    return Images

def generate_video(Images, video_name, img_type,outputPath, fps=30):
    #read the first image of the video to get the size
    image = cv2.imread(Images[img_type][video_name][0])
    pbar = tqdm(range(len(Images[img_type][video_name])))
    video = cv2.VideoWriter(os.path.join(outputPath,f'{video_name}.avi'), cv2.VideoWriter_fourcc(*'DIVX'), fps, (image.shape[1], image.shape[0]))
    for i in pbar:
        image = cv2.imread(Images[img_type][video_name][i])
        pbar.set_description(f'Generating video {video_name}...')
        video.write(image)
        
        
        
    cv2.destroyAllWindows()
    video.release()
    print('Done!')


if __name__ == '__main__':
    #Parse command line arguments: img_location, output_location
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--img_location', help='Location of the images', required=True)
    parser.add_argument('-o', '--output_location', help='Location of the output videos', required=True)
    args = parser.parse_args()

    #remove any weird characters from the path, like spaces, newlines, etc.
    input_img = ''.join(letter for letter in args.img_location if letter.isalnum() or letter in ['/','_','-','.'])
    output_vid = ''.join(letter for letter in args.output_location if letter.isalnum() or letter in ['/','_','-','.'])

    print(f'Input images: {input_img}\nOutput videos: {output_vid}')
    Images = load_images(input_img)
    os.makedirs(output_vid, exist_ok=True)
    for img_type in Images:
        os.makedirs(os.path.join(output_vid, img_type), exist_ok=True)
        for video in Images[img_type]:
            generate_video(Images, video, img_type, os.path.join(output_vid, img_type)) 