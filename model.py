from PySide import QtCore
from obspy.core.stream import Stream
from obspy.core.trace import Trace
from obspy.segy.segy import readSEGY
import numpy as np
import sys


class Model(QtCore.QObject):
    dataChanged = QtCore.Signal()
    def __init__(self, filename = None):
        QtCore.QObject.__init__(self)
        self.fileName = filename
    
    def readData(self):
        temp = readSEGY(self.fileName,headonly=True)
        #print dir(temp)
        #print dir(temp.traces[0])
        #print temp.binary_file_header
        
        self.ntraces = len(temp.traces)
        self.ntimes = len(temp.traces[0].data)
        
        # temporary for testing only
        self.ntraces = 1000
        # Put the traces in a numpy array 
        self.data = np.empty([self.ntimes,self.ntraces])
        for i in range(0,self.ntraces):
            self.data[:,i] = temp.traces[i].data
        
        del temp # just making sure
    def saveData(self, filename = None):
        stream = Stream()
        for i in range(0,self.ntraces):
            curr_trace = self.data[:,i]
            curr_trace = np.require(curr_trace, dtype='float32')
            temp = Trace(data=curr_trace)
            # Attributes in trace.stats will overwrite everything in
            # trace.stats.segy.trace_header
            temp.stats.delta = 0.01
                # Add trace to stream
            stream.append(temp)
        print "Stream object before writing..."
        print stream
        stream.write(filename, format="SEGY", data_encoding=1,
                    byteorder=sys.byteorder)
  
    def setData(self, data = None):
        self.data = data         
        
    def getData(self):
        return self.data  
        
    def getNTraces(self):
        return self.ntraces
    
    def getTLength(self):
        return self.ntimes
        
    def getTrace(self, i = 0):
        return self.data[:,i]
        
    def setTrace(self, i = 0, trace = None):
        if trace:
            self.data[:,i] = trace
            
    def setAGCData(self, data):
        self.agc_data = data

    def get_agc_data(self):
        return self.agc_data

    def set_psd_data(self,psd_estimate):
        self.psd_data = psd_estimate
        
    def get_psd_data(self):        
        return self.psd_data
        
    def get_psd_of_trace(self, i=0):
        return self.psd_data[:,i]
        
    

        

        
    