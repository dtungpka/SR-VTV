import os
#read all files in folder src, check for each subfolder in dst, if found one of them not exist in src or dst, delete it and print its name

#folder stucture:
# src
# [file1, file2, ...]
# dst
#  subfolder1
#   [file1, file2, ...]
# subfolder2
#  [file1, file2, ...]

def equal_data(src, dst):
    #get all files in src
    src_files = []
    for root, dirs, files in os.walk(src):
        for file in files:
            src_files.append(file)
    #get all files in each subfolder in dst
    dst_files = {} #subfolder: [files]
    for root, dirs, files in os.walk(dst):
        if root != dst:
            dst_files[root] = files
    #check if each subfolder in dst has the same files as src
    for subfolder in dst_files:
        for file in dst_files[subfolder]:
            if file not in src_files and file.replace('x4','') in src_files:
                #rename file
                os.rename(os.path.join(subfolder, file), os.path.join(subfolder, file.replace('x4','')))
                print('renaming ' + os.path.join(subfolder, file) + ' to ' + os.path.join(subfolder, file.replace('x4','')))
            if file.replace('x4','') not in src_files:
                print('deleting ' + os.path.join(subfolder, file))
                os.remove(os.path.join(subfolder, file))
    #check if each subfolder in src has the same files as dst
    for file in src_files:
        found = False
        for subfolder in dst_files:
            if ''.join([file.split('.')[-2],'x4.',file.split('.')[-1]]) in dst_files[subfolder]:
                found = True
                break
        if not found:
            print('deleting ' + file)
            os.remove(file)

if __name__ == '__main__':
    equal_data('/work/21010294/VSR/STDO-CVPR2023/dataset/DIV2K_train_HR/', '/work/21010294/VSR/STDO-CVPR2023/dataset/DIV2K_train_LR_bicubic/')
