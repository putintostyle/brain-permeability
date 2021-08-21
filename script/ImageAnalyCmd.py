import cmd
from ImageAnalyzer import *

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

class ImageAnalyzerShell(ImageAnalyzerShellBase, ImageAnalyzer):
    def __init__(self):
        ImageAnalyzerShellBase.__init__(self)
        self.analyzer = ImageAnalyzer
        
        
    def do_select(self, args):
        # dict = {'LF':{'slice_name': 'I70', 'region':[center, radius]}, 'CH':'LF':{'slice_name': 'I70', 'region':[center, radius]}}
        cmds = args.split()
        slice = cmds[0]
        label = cmds[1]
        tmp_dict = {'slice name' : slice, 'regions':self.analyzer.select_region(slice)}
        
        self.analyzer.region[label] = tmp_dict
         # 新增region上去
    def do_regionshow(self, args): 
        # cmds = args.split()

        self.analyzer.regionshow(slice)