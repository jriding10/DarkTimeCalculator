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
# 2020-07-27    JLR     GUI works, Code works, just not together

# Module Versions:
# python version 3.8
# calculator.py
#################################################################################

# standard libraries
import sys
import importlib as imp

import nightTime as nt
import dateAndTime as dnt
import utilities as util

# reload modules (for debugging purposes)
#imp.reload(nt)

# Widget libraries
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QVBoxLayout, QDialog, QLineEdit, QLabel, QComboBox, 
                             QPushButton, QGridLayout, QMessageBox, QCheckBox, QGroupBox, QTableWidget, QTableWidgetItem)
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
        
        bLLayout = QHBoxLayout()
        bLLayout.addWidget(quit)
        bLLayout.addStretch(1)
        
        bRLayout = QHBoxLayout()
        bRLayout.addWidget(calcButton)
        bRLayout.addStretch(1)
        
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
        mainLayout.addLayout(bLLayout, 3, 0, 1, 2)
        mainLayout.addLayout(bRLayout, 3, 1, 1, 2)
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
        
        if validYear:
            self.calculateCH()
            
    def calculateCH(self):
        midday = ' 2:00:00'
        midnight = ' 14:00:00'
        aat = util.createLocation()
        
        
        monthStart, monthEnd = util.monthStartEndPoints(self.month)
        currentMonth = monthStart
    
# Initialise required dictionaries.
        night = {}
        tableVars = {}
        if self.calculateHalfNights:
            firstHalf = {}
            secondHalf = {}

#This while loop cycles through the months requested.
        i = 0
        while currentMonth >= monthStart and currentMonth <= monthEnd:
# cover the fact semester B includes January of the next year
            if self.month == 14:
                if currentMonth == 13:
                    currentMonth = 1
                    self.year += 1
# compute the dates for this month.
            thisMonth = dnt.Dates(currentMonth, self.year)
            thisMonth.numDaysInMonth = thisMonth.numberOfDaysInMonth(currentMonth)
            thisMonth.createDate()
            dates = thisMonth.dates
        
# This while loops over the days of the month and calculates CH
            j = 0
            while j < thisMonth.numDaysInMonth:
                # Create time object
                middayJD = util.convertJD(dates[j], midday)
                midnightJD = util.convertJD(dates[j], midnight)
                night[i] = nt.NightInfo(aat, dates[j], middayJD)
                tableVars[i] = nt.CHvalues(self.year, self.month)

# Calculate the various times to get CH
                night[i].getAstroTimes()
                night[i].getNauticalTimes()
                night[i].getNightLengths()
                night[i].getMoonTimes()
                night[i].moonUp()
                night[i].calculateChiaroscuro()
            
                tableVars[i].date = dates[j]
                tableVars[i].CH = night[i].chiaroscuro
        
# Repeat of above for 1st half of the night. Set end times to midnight.
                if self.calculateHalfNights:
                    firstHalf[i] = nt.NightInfo(aat, dates[i], middayJD)
                    firstHalf[i].getAstroTimes()
                    firstHalf[i].getNauticalTimes()
                    firstHalf[i].astroEnd = midnightJD
                    firstHalf[i].nauticalEnd = midnightJD
                    firstHalf[i].getNightLengths()
                    firstHalf[i].getMoonTimes()
                    firstHalf[i].moonUp()
                    firstHalf[i].calculateChiaroscuro()
                
                    tableVars[i].firstCH = firstHalf[i].chiaroscuro

# Repeat of above for 2nd half of the night. Set start times to midnight.
                    secondHalf[i] = nt.NightInfo(aat, dates[i], middayJD)
                    secondHalf[i].getAstroTimes()
                    secondHalf[i].getNauticalTimes()
                    secondHalf[i].astroStart = midnightJD
                    secondHalf[i].nauticalStart = midnightJD
                    secondHalf[i].getNightLengths()
                    secondHalf[i].getMoonTimes()
                    secondHalf[i].moonUp()
                    secondHalf[i].calculateChiaroscuro()
                        
                    tableVars[i].secondCH = secondHalf[i].chiaroscuro
    
   
            i+=1
            j+=1
            print(dates[i] + '   ' + str(night[i].chiaroscuro))
            currentMonth+=1
        
            filename = calc.fileName()
            if self.saveTXT:
                tableVars.saveToTxtFile(filename, night)
            if self.saveCSV:
                tableVars.saveToCsvFile(filename, night)
        
#        def showCH(self):
#            numRows = len(tableVars)
#        
#            self.chTable = QTableWidget()
#            self.chTable.setRowCount(numRows+2)
#            self.chTable.setColumnCount(3)
#            self.chTable.setItem(0,0, QTableWidgetItem("Date"))
#            self.chTable.setItem(0,1, QTableWidgetItem("CH"))
#            self.chTable.setItem(0,2, QTableWidgetItem("Type"))
            
#            i = 1
#            colour = "bright"
#            while i < numRows:
#                CH = tableVars[i].chiaroscuro
#                self.chTable(i,0, QTableWidgetItem(tableVars[i].date))
#                self.chTable(i,1, QTableWidgetItem(str(CH)))
#                if CH > 0.65:
#                    colour = "bright"
#                elif CH > 0.35:
#                    colour = "grey"
#                else:
#                    colour = "dark"
#                self.chTable(i,2, QTableWidgetItem(colour))
#                i+=1
                
#        exitButton = QPushButton('Quit', self)
#        exitButton.clicked.connect(self.close)
        
#        layout = QHBoxLayout()
#        layout.addWidget(self.chTable)
#        layout.addStretch(1)
#        layout.addWidget(exitButton)
#        layout.addStretch(1)
        
#        self.show()
            
            
#    def createProgressBar(self):
#        self.progressBar = QProgressBar()
#        self.progressBar.setRange(0, 30)
#        self.progressBar.setValue(0)
        
        
    
        

        
        
        
        
if __name__ == "__main__":
    app = QApplication([])
    mainWin = DTC_GUI()
    mainWin.show()
    sys.exit(app.exec_())

        

        



