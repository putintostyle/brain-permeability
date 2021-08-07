import cmd
from ImageAnalyzer import *

class ImageAnalyzerShellBase(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)

class ImageAnalyzerShell(ImageAnalyzerShellBase, analyzer):
    def __init__(self):
        ImageAnalyzerShellBase.__init__(self)
        self.analyzer = analyzer
    
