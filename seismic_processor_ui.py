from PySide import QtGui,QtCore
from view import View
from model import Model
from processor import Processor
import os


class SeismicProcessorUI(QtGui.QMainWindow):
    
    def __init__(self):
        super(SeismicProcessorUI, self).__init__()
        self.mdiArea = QtGui.QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)
        self.init_ui()
        
    def init_ui(self):             
        self.lastPath = os.getcwd()    
        self.create_actions()
        self.create_menus()
        self.Views = []
        self.statusBar()

        self.setGeometry(300, 600, 1050, 850)
        self.setWindowTitle('Seismic Pro')    
        self.show()

    def closeEvent(self,event):
        self.mdiArea.closeAllSubWindows()
        
    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None      

    def create_view(self,p_type = None, fname = None, t_num = 0, region = []):

        self.Views.append( View(plot_type = p_type,filename = fname, model = self.model,
                                trace_num = t_num, region = region) )
        self.mdiArea.addSubWindow(self.Views[len(self.Views)-1])
        self.Views[len(self.Views)-1].show()
       
    def create_actions(self):
        # File Actions #
        self.loadAction = QtGui.QAction('Open', self)
        self.loadAction.setShortcut('Ctrl+O')
        self.loadAction.setStatusTip('Open segy file')
        self.loadAction.triggered.connect(self.open_segy)
       
        self.exitAction = QtGui.QAction('Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)

       # Processing Actions #
        self.powerSpectrumAction = QtGui.QAction('Spectral Density', self)
        self.powerSpectrumAction.setStatusTip('Compute power spectrum of traces')
        self.powerSpectrumAction.triggered.connect(self.run_psd_estimation)        
        self.powerSpectrumAction.setDisabled(True)    
        
        # Processing Actions #
        self.normalMoveOutAction = QtGui.QAction('Periodigram', self)
        self.normalMoveOutAction.setStatusTip('Computes Periodigram')
        self.normalMoveOutAction.triggered.connect(self.run_periodigram)        
        self.normalMoveOutAction.setDisabled(True)    


        self.stackAction = QtGui.QAction('Sparse Deconvolution', self)
        self.stackAction.setStatusTip('Uses Spicking Deconvolution')
        self.stackAction.triggered.connect(self.run_deconvolution)  
        self.stackAction.setDisabled(True)    
      

        self.migrateAction = QtGui.QAction('Migration', self)
        self.migrateAction.setStatusTip('Performs time migration')
        self.migrateAction.triggered.connect(self.run_migration)    
        self.migrateAction.setDisabled(True)    
    

        # View Actions #
        self.surfaceViewAction = QtGui.QAction('Surface', self)
        self.surfaceViewAction.setStatusTip('View as data surface')
        self.surfaceViewAction.triggered.connect(self.surface_view)    
        self.surfaceViewAction.setDisabled(True)    

        self.traceViewAction = QtGui.QAction('Trace', self)
        self.traceViewAction.setStatusTip('View a single trace plot')
        self.traceViewAction.triggered.connect(self.trace_view)    
        self.traceViewAction.setDisabled(True)    

        self.powerSpectrumViewAction = QtGui.QAction('Spectrum ', self)
        self.powerSpectrumViewAction.setStatusTip('View a single trace plot')
        self.powerSpectrumViewAction.triggered.connect(self.psd_view)    
        self.powerSpectrumViewAction.setDisabled(True)    



    def enableActions(self):
        self.surfaceViewAction.setDisabled(False)    
        self.traceViewAction.setDisabled(False)      
        self.powerSpectrumAction.setDisabled(False)   
        self.normalMoveOutAction.setDisabled(False)   
        self.stackAction.setDisabled(False)    
        self.migrateAction.setDisabled(False)    

     
        
    def create_menus(self):
        
        self.menubar = self.menuBar()
        
        # File Menu #
        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(self.loadAction)        
        self.fileMenu.addAction(self.exitAction)        
        
        # Process Menu #
        self.processMenu = self.menubar.addMenu('&Process')
        self.processMenu.addAction(self.powerSpectrumAction) 
        self.processMenu.addAction(self.normalMoveOutAction) 
        self.processMenu.addAction(self.stackAction)         
        self.processMenu.addAction(self.migrateAction)         
        
        # View Menu #
        self.viewMenu = self.menubar.addMenu('&View')
        self.viewMenu.addAction(self.surfaceViewAction) 
        self.viewMenu.addAction(self.traceViewAction)         
        self.viewMenu.addAction(self.powerSpectrumViewAction)         
    
     # define slot calls #
     
    def open_segy(self):
        filename,_ = QtGui.QFileDialog.getOpenFileName(self, "Open Segy File", self.lastPath) 
        # make sure this is a segy file
        _,ext = os.path.splitext(filename)
        self.lastPath, fname = os.path.split(filename)
        if ext != '.segy' and ext != '.sgy':
           errDialog = QtGui.QErrorMessage(self) 
           errDialog.showMessage("File Format Error: File must be SEGY")
           return
        self.model = Model(filename)
        self.model.readData()
        self.run_acg()
        self.create_view('Image',fname)
        self.enableActions()

    def trace_view(self):
        t_num, ok = QtGui.QInputDialog.getInteger(self, self.tr("Trace View"),
                                                    self.tr("Trace Number:"), 0, 0, self.model.getNTraces(), 1)
        if ok:
            self.create_view(p_type = 'TracePlot',t_num = t_num)
            
    def surface_view(self):
        region, ok = QtGui.QInputDialog.getText(self, self.tr("Surface View"),
                                                    self.tr("tr_i tr_e t_i t_e:"),QtGui.QLineEdit.Normal)
        region = str(region)
        region = region.split()
        region = [int(x) for x in region]
        if len(region)!=4:
           errDialog = QtGui.QErrorMessage(self) 
           errDialog.showMessage("You need to enter four elemets")
           return   
        if region[0]>region[1] or region[2]>region[3]:
           errDialog = QtGui.QErrorMessage(self) 
           errDialog.showMessage("Make sure you have entered the dimensions correctly")
           return
        if ok:
            self.create_view(p_type = 'Surface',region = region)        

    def psd_view(self):
        t_num, ok = QtGui.QInputDialog.getInteger(self, self.tr("PSD View"),
                                                    self.tr("Trace Number:"), 0, 0, self.model.getNTraces(), 1)
        if ok:
            self.create_view(p_type = 'PSD',t_num = t_num)


    def run_psd_estimation(self):
        if not hasattr(self,'processor'):
            self.processor = Processor(self.model)  
        self.processor.compute_psd()  
        self.powerSpectrumViewAction.setDisabled(False) 
            
    def run_acg(self):
        if not hasattr(self,'processor'):
            self.processor = Processor(self.model)
        print "running agc"        
        self.processor.automatic_gain_control()
        
    def run_periodigram(self):
        if not hasattr(self,'processor'):
            self.processor = Processor(self.model)
        
    def run_deconvolution(self):
        if not hasattr(self,'processor'):
            self.processor = Processor(self.model)
                       
  
    def run_migration(self):
        if not hasattr(self,'processor'):
            self.processor = Processor(self.model)
        print "running migration"                
        
        
        
        
        
        
        
        
        
        
        
        