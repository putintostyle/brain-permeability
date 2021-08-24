from ImagePreprocessor import *
from sklearn import linear_model

class ImageAnalyzer:
    def __init__(self, workDir, preprocessor, locations = 'default'):
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

    def computeConcerntration(self, VIF = False, ROI_size = None, initial, start_slice, end_slice):
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

        return np.array(c)
    
    def computeKi(self, shape_ROI, c_p, y, drop_list = []):
        Ki = []
        for i in range(shape_ROI):
            c_p_tmp = c_p[:,i]+1e-10
            per_time = 0
            y_t = []
            x_t = []
            for time in range(len(c_p_tmp)):
                if time not in drop_list: 
                    if time <= 16: 
                        per_time += c_p_tmp[time]*(4/60)
                        y_t.append(y[:,i][time])
                        x_t.append(per_time/(c_p_tmp[time]))
                    elif (time>16)&(time<=35):
                        per_time += c_p_tmp[time]*(6/60)
                        y_t.append(y[:,i][time])
                        x_t.append(per_time/(c_p_tmp[time]))
                    elif (time>35)&(time<=41):
                        per_time += c_p_tmp[time]*(8/60)
                        y_t.append(y[:,i][time])
                        x_t.append(per_time/(c_p_tmp[time]))
                    elif (time>41):
                        per_time += c_p_tmp[time]
                        y_t.append(y[:,i][time])
                        x_t.append(per_time/(c_p_tmp[time]))
            x_t = np.array(x_t)
            y_t = np.array(y_t)

            y_t_mean = np.mean(y_t)
            y_t_std = np.std(y_t)

            drop_index = []
            for index in range(len(y_t)):
                if abs(y_t[index]-y_t_mean)>y_t_std:
                    drop_index.append(index)

            y_t = np.delete(y_t, drop_index)
            x_t = np.delete(x_t, drop_index)
    #         plt.scatter(x_t, y_t)
    #         plt.show()
            regr = linear_model.LinearRegression()
    #         print(x_t)
    #         print(y_t)
            regr.fit(x_t.reshape(-1,1), y_t)
            Ki.append(round(regr.coef_[0],5))
        return np.array(Ki)
    
