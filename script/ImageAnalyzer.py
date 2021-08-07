import numpy as np
import matplotlib.pyplot as plt
import subprocess
import time


try:
    import pydicom
except:
    subprocess.run(['pip', 'install',  'pydicom'])
    import pydicom



class ImageAnalyzer:
    def __init__(self, path):
        self.PATH = path
        # "D:\\下載\\gLymph test-20200429T121458Z-001\\gLymph test\\S5010 T2\\"
        
    def tellme(s):
        print(s)
        plt.title(s, fontsize=16)
        plt.draw()
    
        
    def select_region(self, args):
        # usage：select_region

##################################################
# Define a triangle by clicking three points

    self.img = pydicom.read_file(PATH+'I70').pixel_array
plt.clf()
plt.imshow(img, cmap=plt.cm.bone)
plt.gcf().canvas.draw() 
plt.setp(plt.gca(), autoscale_on=False)

tellme('Press enter to start')
motion = plt.waitforbuttonpress()
if motion == True:
    tellme("double click to label")
    # a = plt.ginput(1, timeout=-1, show_clicks=True)
    
    pts = []
    # click_points = 
    # print(click_points)
    # pts.append(np.asarray(plt.ginput(1, timeout=-1, show_clicks=True))[0])
    # print(np.array(pts)[:,0], np.array(pts)[:,1])
    # plt.scatter(np.array(pts)[-1,0], np.array(pts)[-1,1])
    while (len(pts)>=0)&(plt.waitforbuttonpress() != True):
        # click_points = ()
        pts.append(np.asarray(plt.ginput(1, timeout=-1,  show_clicks=True, mouse_add = 1))[0])
        # print(pts)
        plt.scatter(np.array(pts)[-1,0], np.array(pts)[-1,1])
        plt.gcf().canvas.draw() 
        if len(pts)>=2: 
            plt.plot(np.array(pts)[-2:, 0] ,np.array(pts)[-2:, 1],  'r', lw=2)
            plt.gcf().canvas.draw()
        tellme("double space to leave double click to label")
        if ((len(pts)>=2) & (pts[0] == pts[-1]).all() ):
            plt.close()
            break
else:
    tellme('Please tab to begin')
    tellme('tab to begin')

fig, ax = plt.subplots()
ax.imshow(img, cmap=plt.cm.bone)
lengthOfpts = len(pts)
for pt_idx in range(lengthOfpts):
    if pt_idx+1 < lengthOfpts:
        ax.plot([pts[pt_idx][0], pts[pt_idx+1][0]], [pts[pt_idx][1], pts[pt_idx+1][1]], 'r', lw=2)
    else:
        ax.plot([pts[pt_idx][0], pts[0][0]], [pts[pt_idx][1], pts[0][1]], 'r', lw=2)
plt.show()