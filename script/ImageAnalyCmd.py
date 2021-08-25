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
        self.result = {} 
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
        # usage concerntration -all 64 -LR 64
        cmds = args.split()

        if '-all' in cmds:
            series = cmds(cmds.index[-all]+1)
        else:
            print('need parameters, for example, -all 64')
        # ToDo : convert input to variables
        self.Ki = []
        self.analyzer.dict = self.region

        for label in self.analyzer.dict:
            self.analyzer.label = label
            
            start_ROI = self.region[label]['slice name']
            start_VIF = self.region['VIF']['slice name']

            self.initROI = self.analyzer.storeRegion(label, start_ROI)
            self.initVIF = self.analyzer.storeRegion(start_VIF)

            self.c_p = self.analyzer.computeConcerntration(True,
                                                            len(self.initROI),
                                                            self.initVIF,
                                                            start_VIF,
                                                            start_VIF+series,
                                                            )
            purturbList = [[random.randint(-1, 1), random.randint(-1, 1)] for i in range(3)]

            for purturb in purturbList:
                self.c_t = self.analyzer.computeConcerntration(self.initROI, 
                                                            start_ROI,
                                                            start_ROI+series,
                                                            purturb)

                
                self.y = (self.c_t+1e-10)/(self.c_p+1e-10)

                self.Ki.append(self.analyzer.computeKi(len(self.initROI),
                                                self.c_p,
                                                self.y))
            removeNoise, bins, positive, negative = self.analyzer.noiseElimation(self.Ki)
            result = {'remove':removeNoise, 'bins':bins, 'positive' :positive, 'negative' :negative}
            self.result[label] = result
    
    def do_stat(self, args):
        # usage stat 
        cmds = args.split()
        if '-all' in cmds:
            for label in self.analyzer.dict:
                self.analyzer.plotStat(self.result, label, )


        
        

