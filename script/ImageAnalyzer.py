from ImagePreprocessor import *


class ImageBase:
    def __init__(self, workDir, selectFileName, fileDict):
        self.selectFileName = selectFileName
        self.fileDict = fileDict
        self.workDir = workDir
        # fileDict = {'LF':{slice: 70,region:[]}}
        pass
    
        
    def storeROI(self,label):
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
    
class ImageAnalyzer(ImageBase):
    def __init__(self, workDir, selctFileName, locations):
        super().__init__()
        self.img = ImagePreprocessor(self.workDir, self.selectFileName).image_calibration(locations)
        pass
    def computeConcerntration(self, initROI):
        