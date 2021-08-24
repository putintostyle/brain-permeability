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
    def do_concerntration(self, args):
        # usage concerntration -label LR -start 70 -end 140
        cmds = args.split()
        self.analyzer.dict = self.region
        self.initROI = self.analyzer.storeRegion(ROI_slice)
        self.initVIF = self.analyzer.storeRegion(VIF_slice)
        self.c_t = self.analyzer.computeConcerntration(self.initROI, start, end)
        self.c_p = self.analyzer.computeConcerntration(self.initVIF, start, end)
        

        
        

