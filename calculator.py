#################################################################################
#                                                                               #
#                               calculator.py                                   #
#                                                                               #
#################################################################################

# Purpose:
# Calculates the chiaroscuro - the fraction of time the night that is dark. 
# Completes this fraction for half nights to aid scheduling. This fraction is 
# calculated for the whole night and half night to aid with half-night programs.

# Meant to be used with  

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

# Module Versions:
# python version 3.7
# nightTime.py, utilities.py, dateAndTime.py, DTC_GUI.py 
#################################################################################
# modules found in this directory
import utilities as util
import nightTime as nt
import dateAndTime as dnt

# standard libraries
import csv
from astropy.time import Time
import importlib as imp

# reload modules (for debugging purposes)
imp.reload(dnt)
imp.reload(util)
imp.reload(nt)

# run the next two lines occassionally for the most up-to-date rise/set times
# from astroplan import download_IERS_A   # Best precision data (arcseconds)
# download_IERS_A()

# Location of the AAT according to the Observer's Guide 1991. This concurs with 
# the location stored in astroplan library.
# longitude = 149deg 3min 58sec E
# latitude = 31deg 16min 37sec S
# altitude = 1165m - this is if the horizon is at sea level. Consider using 670m 
# with the local horizon. Difference in dark time under a minute. Difference in CH
# unnoticable.

#longitude = 149.0 + 3.0/60 + 58.0/3600
#latitude = -1*(31.0 + 16.0/60 + 37.0/3600)
#altitude = 1164
#aat = util.createObservatory(longitude, latitude, altitude)

        self.midday = ' 2:00:00'
        self.midnight = ' 14:00:00'
        

    
#################################################################################### 

        
    
# won't write for some reason
#else:
#    util.readableTableAllCH(night, firstCH, secondCH, filename)




