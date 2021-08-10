import cmd
from ImageAnalyzer import *

class ImageAnalyzerShellBase(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)

class ImageAnalyzerShell(ImageAnalyzerShellBase, analyzer):
    def __init__(self):
        ImageAnalyzerShellBase.__init__(self)
        self.analyzer = analyzer
    def do_select(self, args):
        cmds = args.split()
        slice = cmds[0]
        label = cmds[1]
        self.analyzer.select(slice, label) # 新增region上去
    def do_regionshow(self, args): 
        slef.analyzer.regionshow(slice)