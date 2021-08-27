import numpy as np
import matplotlib.pyplot as plt
import subprocess
import time
from ImageSelector import *
import os
from scipy.signal import find_peaks
try:
    import pydicom
except:
    subprocess.run(['pip', 'install',  'pydicom'])
    import pydicom
            

class ImagePreprocessor:
    def __init__(self, workDir):
        self.path = workDir
        # "D:\\下載\\gLymph test-20200429T121458Z-001\\gLymph test\\S5010 T2\\"
    
    def select_region(self, slice, manRadius = False):
        fig, ax = plt.subplots()
        img = pydicom.read_file(os.path.join(self.path, slice)).pixel_array
        ax.imshow(img, cmap = plt.cm.bone)
        wm = window_motion(fig, ax, manRadius)
        wm.connect()
        plt.show()
        return wm.region
        # usage：select_region
       
    def image_calibration(self, fileName, fatLocation):
        img = pydicom.read_file(os.path.join(self.path, fileName))
        peaks1, _ = find_peaks(img[fatLocation[0]], height=0)
        peaks2, _ = find_peaks(img[fatLocation[1]], height=0)
        peaks3, _ = find_peaks(img[fatLocation[2]], height=0)
        
        fat_array = [peaks1[0],peaks1[-1], peaks2[0],peaks2[-1],peaks3[0],peaks3[-1]] #store all the peaks
        fat_array = [i for i in fat_array if i!=0]
        fat_array.remove(max(fat_array))
        fat_array.remove(min(fat_array))

        return img/np.mean(fat_array)
##################################################
# Define a triangle by clicking three points
# imga = ImageAnalyzer(workDir = '../S5010 T2', selectFileName = 'I70')
# imga.imgSetting()
# print(imga.img)
# imga.region = {'LR':{'slice name' : 70, 'regions':imga.select_region()}}
# imga.show()
'''
def show(self, indicate = None):
        # usage:indicate = ['LF', 'BG']
        # ToDo : select slice
        
        if indicate != None:
            for label in indicate:
                slice = self.region[label]['slice name']
                regions = self.region[label]['regions']
                fig, ax = plt.subplots()
                img_arr = pydicom.read_file(os.path.join(self.path, slice)).pixel_array
                ax.imshow(img_arr, cmap = plt.cm.bone)
                for cir in regions:
                    
                    ax.add_patch(Circle((cir[0], cir[1]), 1/2*cir[2], fill=True, color='grey') )
        else:
            print(self.region)
            for label, region in self.region.items():
                fig, ax = plt.subplots()
                slice = self.region[label]['slice name']
                img_arr = pydicom.read_file(os.path.join(self.path, slice)).pixel_array
                ax.imshow(img_arr, cmap = plt.cm.bone)
                for cir in region['regions']:
                    print(cir)
                    ax.add_patch(Circle((cir[0], cir[1]), 1/2*cir[2], fill=True, color='grey') )
                plt.show()
'''