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
        self.prompt = "> "
        self.intro  = None  ## defaults to None

    ## Command definitions ##
    def do_hist(self, args):
        """Print a list of commands that have been entered"""
        print(self._hist)

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    ## Command definitions to support Cmd object functionality ##
    def do_EOF(self, args):
        """Exit on system end of file character"""
        return self.do_exit(args)

    def do_shell(self, args):
        """Pass command to a system shell when line begins with '!'"""
        os.system(args)

    def do_help(self, args):
        """Get help on commands
           'help' or '?' with no arguments prints a list of commands for which help is available
           'help <command>' or '? <command>' gives help on <command>
        """
        ## The only reason to define this method is for the help text in the doc string
        cmd.Cmd.do_help(self, args)

    ## Override methods in Cmd object ##
    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}

    def postloop(self):
        """Take care of any unfinished business.
           Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)   ## Clean up command completion
        print("Exiting...")

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
        """
        self._hist += [ line.strip() ]
        return line

    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
           If you want to do some post command processing, do it here.
        """
        return stop

    def emptyline(self):    
        """Do nothing on empty input line"""
        pass

    def default(self, line):       
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        try:
            exec(line) in self._locals, self._globals
        except Exception as e:
            print(e.__class__, ":", e)

    # shortcuts
    do_quit = do_exit
    do_q = do_quit
    do_history = do_hist

class ImageAnalyzerShell(ImageAnalyzerShellBase):
    def __init__(self, workDir):
        ImageAnalyzerShellBase.__init__(self)
        
        self.preprocessor = ImagePreprocessor(workDir)
        self.fatCut = []
        self.analyzer = ImageAnalyzer(workDir, self.preprocessor, self.fatCut)
        self.region = {}
        self.result = {}
    def do_fat(self, args):
        cmds = args.split()
        if len(cmds) != 3:
            print('please specify three cuts, for example , fatCut 70 80 90')
        else:
            self.fatCut.append([int(i) for i in cmds])
        
    def do_select(self, args):
        # usage select 70 LF --manual-radius
        # dict = {'LF':{'slice_name': 'I70', 'region':[center, radius]}, 'CH':{'slice_name': 'I70', 'region':[center, radius]}}
        cmds = args.split()
        slice = cmds[0]
        label = cmds[1]
        if '--manual-radius' in cmds:
            tmp_dict = {'slice name' : slice, 'regions':self.preprocessor.select_region(slice,  manRadius=True)}
        else:
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


        
        

