from PySide import QtCore
import numpy as np
from scipy import signal, fftpack
import sys

epsi = sys.float_info.epsilon

class Processor(QtCore.QObject):
    def __init__(self, model = None):
        QtCore.QObject.__init__(self)
        self.model = model
        
    def automatic_gain_control(self):
        data = self.model.getData()
        data = data-np.amin(data)
        (ntime,ntrace) = data.shape
        # intialize a filter window
        wlength = 21
        window = signal.boxcar(wlength)
        gain_data = np.empty([ntime,ntrace])
        # first filter than divide
        for i in range(0,ntrace):
            #gain_data[:,i] = signal.convolve(data[:,i],window,'same') 
            gain_data[:,i] = signal.fftconvolve(data[:,i],window,'same') 
        # add a small number before dividing (in case of zeros)
        gain_data = gain_data+epsi
        gain_data = data/gain_data
        
        #tmp = '/home/amin/Dropbox/research-code/seismic/code/gain_data.txt'
        #np.savetxt(tmp,gain_data,delimiter='\t')
        self.model.setAGCData(gain_data)

    def compute_psd(self):
        data = self.model.getData()
        (ntime,ntrace) = data.shape
        psd_estimate = np.empty([ntime,ntrace])
        for i in range(0,ntrace):
            psd_estimate[:,i]  = np.fft.fftshift(np.square(np.absolute(fftpack.fft(data[:,i]))))

        self.model.set_psd_data(psd_estimate)
        print "finished psd estimation"
        