from PySide import QtGui
from model import Model

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as Toolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt

class View(QtGui.QWidget):


    def __init__(self, parent = None, width=5, height=4, dpi=80, filename = None, model = None,
                        plot_type = 'Image', trace_num = None):
        # plot paramters #                                        
        self.t_num = trace_num

        # connect model signal #
        self.model = model
        self.model.dataChanged.connect(self.update_views)
        
        # create a dictionary of views 
        self.view_options = {'Image': self.view_image,
                             'TracePlot': self.view_trace,
                             'PSD': self.view_psd,
                             'Surface':self.view_surface}
        super(View,self).__init__(parent)
        
        # make the figure
        self.figure = Figure((width, height), dpi)
        fig_color = (1.0, 1.0, 1.0, 1.0)
        self.figure.set_facecolor(fig_color)
        # create the canvas
        self.canvas = Canvas(self.figure)
        self.canvas.setParent(self)
        
        # create the toolbar and tie it to the canvas
        self.toolbar = Toolbar(self.canvas, self)
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        if filename:
            self.setWindowTitle(plot_type+': '+filename) 

        if plot_type == 'Surface':
            self.axes = self.figure.gca(projection='3d')
        else:
            self.axes = self.figure.add_subplot(111)
            
        self.axes.hold(False)

        self.view_options[plot_type]()
        self.canvas.show()   

    def view_image(self):
        self.axes.imshow(self.model.get_agc_data(),cmap = cm.coolwarm)
        self.axes.set_xticklabels([])
        self.axes.set_yticklabels([])  
        self.axes.set_xticks([])
        self.axes.set_yticks([])        
        self.axes.set_xlabel('source channel')        
        self.axes.set_ylabel('time')        
            
        
    def view_trace(self):
        print self.t_num
        y = self.model.getTrace(self.t_num)
        x = np.arange(len(y))
        self.axes.fill(x,y,'r',linewidth = 0)
        self.axes.set_xlabel('time')        
        self.axes.set_ylabel('amplitude') 
        self.axes.set_xlim(0,len(x))   
        self.axes.grid(True)    
    
    def view_surface(self):
        
        x = np.arange(self.model.getNTraces())
        y = np.arange(self.model.getTLength())       
        x, y = np.meshgrid(x, y)
        z = self.model.get_agc_data()
        self.axes.plot_surface(x,y,z, rstride=1, cstride=1, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)

    def view_psd(self):
        y = self.model.get_psd_of_trace(self.t_num)
        x = np.arange(-len(y)/2,len(y)/2)
        print x.shape
        print y.shape
        self.axes.semilogy(x,y,'r', linewidth  = 1)
        self.axes.set_xlabel('frequency')        
        self.axes.set_ylabel('spectral density')        
        self.axes.set_xlim(-len(x)/2,len(x)/2)   
        self.axes.grid(True)            
       
   
    def update_views(self):
        print "updating views"

 

























