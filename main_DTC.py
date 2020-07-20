#################################################################################
#                                                                               #
#                               main_DTC.py                                     #
#                                                                               #
#################################################################################

# Purpose:
# Calculates the chiaroscuro - the fraction of time the night that is dark. 
# Completes this fraction for half nights to aid scheduling. This fraction is 
# calculated for the whole night and half night to aid with half-night programs.

# This version of the program is designed to be used with the GUI

# Bright:       CH < 0.35
# Grey:         0.35 <= CH < 0.65
# Dark:         CH >= 0.65

# Change Log:
# 2020-06-28    JLR     Single day version complete
# 2020-07-07    JLR     Changed most time scenarios to JD
#                       Implemented classes
# 2020-07-10    JLR     Broke program into module files
# 2020-07-13    JLR     Calculates CH to some accuracy. Also calculates CH for
#                       the beginning and end halves of the night.
# 2020-07-20    JLR     Began adding the GUI

# Module Versions:
# python version 3.8
# nightTime.py, utilities.py, dateAndTime.py, DTC_GUI.py 
#################################################################################
# modules found in this directory
#import utilities as util
#import nightTime as nt
#import dateAndTime as dnt

# standard libraries
import sys
#import csv
#from astropy.time import Time
#import importlib as imp

# reload modules (for debugging purposes)
#imp.reload(dnt)
#imp.reload(util)
#imp.reload(nt)

# Widget libraries
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
from PyQt5.QtCore import QSize 

class DTC_GUI(QDialog):
    def __init__(self, parent = None):
        super(DTC_GUI,self).__init__(parent)
        
        self.setMinimumSize(QSize(600, 200))    
        self.setWindowTitle("Chiaroscuro Calculator") 

        layout = QHBoxLayout()
        self.yearLine = QLineEdit(self)
        yearLabel = QLabel(self)
        yearLabel.setText('Year:')
        yearLabel.setBuddy(self.yearLine)
        
        #self.yearLine.move(40, 20)
        self.yearLine.resize(40, 24)
        #yearLabel.move(10, 20)
        
        
            
        optionsList = ['January', 
                       'Febuary', 
                       'March',
                       'April',
                       'May',
                       'June',
                       'July',
                       'August',
                       'September',
                       'October',
                       'November',
                       'December',
                       'Semester A',
                       'Semester B']
        
        self.monthSemester = QComboBox()
        self.monthSemester.clear()
        self.monthSemester.addItems(optionsList)
        
        #self.monthSemester.move(80, 20)
        #self.monthSemester.resize(100, 24)
        layout.addWidget(self.yearLine)
        layout.addWidget(self.monthSemester)
        
        
        
        
        #self.createTopLeftGroup()
        #self.createTopRightGroup()
        #self.createBottomLeftGroup()
        #self.createBottomRightGroup()
        #self.createProgressBar()

        pybutton = QPushButton('Calculate', self)
        pybutton.clicked.connect(self.clickMethod)
        #pybutton.resize(100,24)
        #pybutton.move(80, 60)        
        layout.addWidget(pybutton)
        self.setLayout(layout)
        
        
    def clickMethod(self):
        getYear = self.yearLine.text()
        getMonth = str(self.monthSemester.currentText())
        getMNum = int(self.monthSemester.currentIndex())+1
        print("Current month is: " + str(getMNum))
  
        
if __name__ == "__main__":
    app = QApplication([])
    mainWin = DTC_GUI()
    mainWin.show()
    sys.exit(app.exec_())
        
        
   
    # create groups of widgets
        #self.createTopLeftGroup()
        #self.createMiddleLeftGroup()
        #self.createBottomLeftGroup()
        #self.createTopRightGroup()
        #self.createMiddleRightGroup()
        #self.createBottomRightGroup()
        #self.createProgressBar()
    
    #def createTopLeftGroup(self):
        #self.topLeftGroup = QGroupBox("Group 1")
        #self.yearLine = QLineEdit()
        #self.yearLabel = QLabel("Year:")
        #self.yearLabel.setBuddy(yearLine)
        

        



