from ImagePreprocessor import *

class ImageAnalyzer:
    def __init__(self, workDir, locations = 'default', preprocessor):
        self.fileName = None
        self.init_ROI = None
        self.dict = None
        self.path = workDir
        self.img = None
        self.label = None
        self.locations = locations
        self.preprocessor = preprocessor

    def imageCal(self, slice):
        self.img = self.preprocessor.image_calibration(slice, self.locations)

    def storeRegion(self, label, slice):
        self.imageCal(slice) # cal image
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
        return np.array(ROI)

    def initialRegion(self, slice):
        if self.fileName == None:
            print('add a file name')
        else:
            return self.storeRegion(self.label, slice = "") # here to provide label and slice

    def computeConcerntration(self, VIF = False, ROI_size, initial, start_slice, end_slice):
        c = []
        for sliceNum in range(start_slice, end_slice):
            ROI_t = self.storeROI(self.label, sliceNum)
            c_t = np.zeros(len(ROI_t))
            for i in range(len(c_t)):
                if (ROI_t[i] == 0) & (initial[i] == 0):
                        c_t[i] = 0
                else:
                    c_t[i] = -np.log(ROI_t[i]/initial[i])
                if VIF:
                    c.append([np.mean(c_t) for i in range(ROI_size)])
                else:
                    c.append(c_t)

        c = np.array(self.c_t)
