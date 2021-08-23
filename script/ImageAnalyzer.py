from ImagePreprocessor import *

class ImageAnalyzer:
    def __init__(self, workDir):
        self.fileName = None
        self.initROI = None
        self.dict = None
        self.path = workDir
        self.img = None
        self.label = None
    def imageCal(self, locations):
        image_arr = pydicom.read_file(os.path.join(self.path, self.fileName)).pixel_array
        return 

    def storeROI(self, label):
        ROI = []
        for selectROI in self.fileDict[label]['regions']:
            for i in range(0,144):
                for j in range(0,144):
                    if (i-selectROI[0])**2+(j-selectROI[1])**2<=selectROI[2]**2:
                        if self.img[i][j] == 0:
                            tmp = self.img[i-3:i+2,j-3:j+2]
                            ROI.append(np.mean(tmp)+1e-10)
                        else:
                            ROI.append(self.img[i][j])
        return ROI

    def initialROI(self):
        if self.fileName == None:
            print('add a file name')
        else:
            self.initROI = self.storeROI(self.label)

    def computeConcerntration(self, initROI):
        if self.fileName == None:
            print('add a file name')
        else:
