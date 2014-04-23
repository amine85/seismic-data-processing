#!/home/amin/Enthought/Canopy_64bit/User/bin/python
# -*- coding: utf-8 -*-

"""

"""
import sys
from seismic_processor_ui import SeismicProcessorUI       
from PySide import QtGui
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = SeismicProcessorUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
