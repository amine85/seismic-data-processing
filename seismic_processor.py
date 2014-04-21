#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""
import sys
import SeismicProcessorUI       
from PySide import QtGui
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = SeismicProcessorUI.SeismicProcessorUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()