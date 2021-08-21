import numpy as np
import matplotlib.pyplot as plt
import subprocess
import time
from ImageSelector import *

try:
    import pydicom
except:
    subprocess.run(['pip', 'install',  'pydicom'])
    import pydicom



class ImageAnalyzer:
    def __init__(self, image_array):
        # self.PATH = path
        self.img = image_array
        self.fig, self.ax = plt.subplots()
        self.region = {}
        # "D:\\下載\\gLymph test-20200429T121458Z-001\\gLymph test\\S5010 T2\\"
        
    def select_region(self):
        self.ax.imshow(self.img, cmap = plt.cm.bone)
        wm = window_motion(self.fig, self.ax)
        wm.connect()
        plt.show()
        return wm.region
        # usage：select_region
    def show(self, indicate = None):
        # usage:indicate = ['LF', 'BG']
        # ToDo : select slice
        fig, ax = plt.subplots()
        ax.imshow(self.img, cmap = plt.cm.bone)
        if indicate != None:
            for label in indicate:
                slice = self.region[label]['slice_number']
                regions = self.region[label]['regions']
                for cir in regions:
                    
                    ax.add_patch(Circle((cir[0], cir[1]), 1/2*cir[2], fill=True, color='grey') )
        else:
            print(self.region)
            for _, region in self.region.items():
                for cir in region['regions']:
                    print(cir)
                    ax.add_patch(Circle((cir[0], cir[1]), 1/2*cir[2], fill=True, color='grey') )
        plt.show()

            
    def image_calibration(self):
        # calibrate from fat
        if 'fat' in self.region:
            print('please select regions of fat for calibration')
        else:
            
        # pass

##################################################
# Define a triangle by clicking three points
imga = ImageAnalyzer(pydicom.read_file('../S5010 T2/I70').pixel_array)
imga.region = {'LR':{'slice name' : 70, 'regions':imga.select_region()}}
imga.show()