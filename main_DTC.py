#################################################################################
#                                                                               #
#                               main_DTC.py                                     #
#                                                                               #
#################################################################################

# Purpose:
# Calculates the chiaroscuro - the fraction of time the night that is dark. 
# Completes this fraction for half nights to aid scheduling. This fraction is 
# calculated for the whole night and half night to aid with half-night programs.

# This version of the program is the GUI

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
# calculator.py
#################################################################################

# standard libraries
import sys
import calculator as calc
import importlib as imp

# reload modules (for debugging purposes)
#imp.reload(calc.calculator)

# Widget libraries
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QVBoxLayout, QDialog, QLineEdit, QLabel, QComboBox, 
                             QPushButton, QGridLayout, QMessageBox, QCheckBox, QGroupBox)
from PyQt5.QtCore import QSize 

class DTC_GUI(QDialog):
    def __init__(self, parent = None):
        super(DTC_GUI,self).__init__(parent)
        
        self.year = 0
        self.month = 0
        self.calculateHalfNights = False
        self.saveCSV = False
        self.saveTXT = False
        
        self.setWindowTitle("Chiaroscuro Calculator") 

        self.yearLine = QLineEdit(self)
        yearLabel = QLabel(self)
        yearLabel.setText('Year:')
        yearLabel.setBuddy(self.yearLine)
        
        self.yearLine.resize(40, 24)
                
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
        
   
        layout = QHBoxLayout()
        layout.addWidget(yearLabel)
        layout.addWidget(self.yearLine)
        layout.addStretch(1)
        layout.addWidget(self.monthSemester)

        self.topLeftGroup = QGroupBox("Chiaroscuro")
        self.halfNights = QCheckBox("Also calculate half night CHs")
        
        tLLayout = QVBoxLayout()
        tLLayout.addWidget(self.halfNights)
        tLLayout.addStretch(1)
        self.topLeftGroup.setLayout(tLLayout)
        
        self.topRightGroup = QGroupBox("Save:")
        self.csvSave = QCheckBox(".csv file")
        self.txtSave = QCheckBox(".txt file")
        
        tRLayout = QVBoxLayout()
        tRLayout.addWidget(self.csvSave)
        tRLayout.addWidget(self.txtSave)
        tRLayout.addStretch(1)
        self.topRightGroup.setLayout(tRLayout)
        
        quit = QPushButton('Quit', self)
        quit.clicked.connect(self.close)
        calcButton = QPushButton('Calculate', self)
        calcButton.clicked.connect(self.clickMethod)
        
        bLayout = QHBoxLayout()
        bLayout.addWidget(quit)
        bLayout.addWidget(calcButton)
        calcButton.move(0, 100)
        bLayout.addStretch(1)
        
        self.midLeftGroup = QGroupBox()
        self.loadIERSA = QCheckBox('Update IERS_A file')
        
        mLLayout = QVBoxLayout()
        mLLayout.addWidget(self.loadIERSA)
        mLLayout.addStretch(1)
        self.midLeftGroup.setLayout(mLLayout)
        
#        self.createProgressBar()
                
        mainLayout = QGridLayout()
        mainLayout.addLayout(layout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroup, 1, 0)
        mainLayout.addWidget(self.topRightGroup, 1, 1)
        mainLayout.addWidget(self.midLeftGroup, 2, 0)
        mainLayout.addLayout(bLayout, 3, 0, 1, 2)
        self.setLayout(mainLayout)
            
    def clickMethod(self):
        validYear = False
               
        getYear = self.yearLine.text()
        try:
            self.year = int(getYear)
        except ValueError:
            alert = QMessageBox()
            alert.setText("Year must be an integer.")
            alert.exec_()
        
        if self.year < 1900 or self.year > 2100:
            alert = QMessageBox()
            alert.setText("Year must be inbetween 1900 and 2100")
            alert.exec_()
        else:
            validYear = True

        getMonth = str(self.monthSemester.currentText())
        self.month = int(self.monthSemester.currentIndex())+1
        self.calculateHalfNights = self.halfNights.isChecked()
        self.saveCSV = self.csvSave.isChecked()
        self.saveTXT = self.txtSave.isChecked()
        
        if self.loadIERSA.isChecked():
            from astroplan import download_IERS_A
            download_IERS_A()
                
        #print("It is " + str(self.month) + " of " + str(self.year) + "\n")
        #print("Half nights is " + str(self.calculateHalfNights))
        
        #if validYear:
        #    calc.calculator(self.year, self.month, self.calculateHalfNights, self.saveCSV, self.saveTXT)
            
#    def createProgressBar(self):
#        self.progressBar = QProgressBar()
#        self.progressBar.setRange(0, 30)
#        self.progressBar.setValue(0)
        
        
    
        

        
        
        
        
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
        

        



