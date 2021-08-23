from ImagePreprocessor import *

class ImageAnalyzer:
    def __init__(self, workDir, locations = 'default', preprocessor):
        self.fileName = None
        self.initROI = None
        self.dict = None
        self.path = workDir
        self.img = None
        self.label = None
        self.locations = locations
        self.preprocessor = preprocessor
        self.initROI = None

    def imageCal(self):
        self.img = self.preprocessor.image_calibration(self.fileName, self.locations)
    def storeROI(self, slice):
        if self.img == None:
            self.imageCal()
        ROI = []
        for selectROI in self.fileDict[self.label]['regions']:
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
            return self.storeROI(self.label)

    def computeConcerntration(self):
        self.initialROI()
