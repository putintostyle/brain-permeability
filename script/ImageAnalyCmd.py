import cmd
from ImageAnalyzer import *
from ImageSetting import *
''' 
workflow:
if rename:
    rename
select LF
select ref
regions = []
select show
imagecal from ref
image analysis
result show
'''

class ImageAnalyzerShellBase(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)

class ImageAnalyzerShell(ImageAnalyzerShellBase):
    def __init__(self, workDir):
        ImageAnalyzerShellBase.__init__(self)
        
        self.preprocessor = ImagePreprocessor(workDir)
        self.analyzer = ImageAnalyzer(workDir, self.preprocessor)
        self.region = {}
          
    def do_select(self, args):
        # usage select 70 LF
        # dict = {'LF':{'slice_name': 'I70', 'region':[center, radius]}, 'CH':{'slice_name': 'I70', 'region':[center, radius]}}
        cmds = args.split()
        slice = cmds[0]
        label = cmds[1]
        tmp_dict = {'slice name' : slice, 'regions':self.preprocessor.select_region(slice)}
        
        self.region[label] = tmp_dict
         # 新增region上去
    def do_regionshow(self, args): 
        
        pass
    def do_computation(self, args):
        # usage concerntration -label LR -start 70 -end 140
        cmds = args.split()
        # ToDo : convert input to variables
        self.Ki = []
        self.analyzer.dict = self.region
        self.initROI = self.analyzer.storeRegion(ROI_slice)
        self.initVIF = self.analyzer.storeRegion(VIF_slice)
        self.c_t = self.analyzer.computeConcerntration(self.initROI, 
                                                       start_ROI,
                                                       end_ROI)

        self.c_p = self.analyzer.computeConcerntration(self.initVIF,
                                                       VIF = True,
                                                       ROI_size = len(self.ROI),
                                                       start_VIF,
                                                       end_VIF)
        self.y = (self.c_t+1e-10)/(self.c_p+1e-10)

        self.Ki.append(self.analyzer.computeKi(len(self.initROI),
                                          self.c_p,
                                          self.y))
        self.removeNoise, self.bins, self.positive, self.negative = self.analyzer.noiseElimation(self.Ki)
        
        


        
        

