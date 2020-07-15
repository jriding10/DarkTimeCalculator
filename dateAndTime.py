# Purpose:
# Contains the code for the class CreateDates
#
# Change Log:
# 2020-07-07    JLR     Copied from DTU.py
#
# Module versions: 
# python version 3.7

import math as m
import numpy as np
from astropy.time import Time

class Dates:
    def __init__ (self, month, year):
        self.month = month
        self.year = year
        self.numDaysInMonth = 31
        self.dates = [0] * 31

    def getMonthName(self):
        monthNames = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }

        return monthNames[self.month]

    def numberOfDaysInMonth(self, month):
        thirty = [4, 6, 9, 11]
        thirtyOne = [1, 3, 5, 7, 8, 10, 12]

        if month in thirty:
            numDaysThisMonth = 30
        elif month in thirtyOne:
            numDaysThisMonth = 31
        else:       
            if self.year % 4 == 0:
                if self.year % 100 != 0 or self.year % 400 == 0:
                    numDaysThisMonth = 29
            else:
                numDaysThisMonth = 28

        return numDaysThisMonth

    def createDate(self):
        numDays = self.numDaysInMonth + 1
        days = list(range(1, numDays))
        months = [self.month] * numDays
        years = [self.year] * numDays
        
        self.dates = [None] * numDays
        i = 0
        while i < numDays-1:
            self.dates[i] = str(years[i]) + '-' + str(months[i]) + '-' + str(days[i])
            i+=1

