#!/usr/bin/env python
#title           :open_csu_slits.py
#description     :This script opens the alignment boxes on a MOSFIRE mask to check if your alignment stars are in the neighborhood of the alignment boxes.
#author          :E. Manjavacas
#date            :December 10, 2019
#version         :1.0
#usage           :python open_csu_slits.py
#notes           :
#python_version  :2.6.6
#==============================================================================
# importing needed packages
#from .core import *
#from .mask import *
#from .mechs import *
#from .detector import *
#import csu
from core import *
from csu import *
#from .analysis import *
import os
from decimal import Decimal
import subprocess
import time
#==============================================================================

def open_csu_slits(slitwidth=0.7):

# Unless otherwise defined, we assume that the slitwidht is 0.7"

    #slitwidth_mm = (slitwidth+0.2)*0.7256
    slitwidth_mm = 0.65
    print(slitwidth_mm)
    print("Open alignment boxes to 9-10 arcsec")

# We determine the position of the odd and even CSU bars, and their difference, to determine the width of the slits:

for i in range(1,47):

    # Position of the even bars:

    even_bar = get(f"B{2*i:02d}POS", 'mcsus', mode=float)
    print('Position even bar: ', even_bar)


    # Position of the odd bars:

    odd_bar = get(f"B{2*i-1:02d}POS", 'mcsus', mode=float)
    print('Position odd bar: ',odd_bar)

    # Difference of both positions, to determine the width of the all the slits:

    Diff_Bars = abs(even_bar-odd_bar)
    print('Difference between bars ' + "{0:0=2d}".format(2*i-1) +' and ' + "{0:0=2d}".format(2*i) + ' in mm :' , Diff_Bars)

    # Open the bars if the difference beteween the bars is bigger than 3 arcsec (2.1768 mm), and smaller than 354.0 arcsec (250.33 mm):

    if Diff_Bars > 0.65 and Diff_Bars < 250.33:
        print('Open the alingment boxes!')
        print(' ')

        # Open odd bars by 2.5 arcseconds (1.814mm)
        new_pos_odd = odd_bar - 1.814
        print('Opening odd bars 2.5 arcsec')        
        set('B'+"{0:0=2d}".format(2*i-1)+'TARG',str(new_pos_odd),service='mcsus', wait=True)

        # Open even bars by 2.5 arcseconds (1.814mm)
        new_pos_even = even_bar+1.814
        print('Opening even bars 2.5 arcsec')
        set('B'+"{0:0=2d}".format(2*i)+'TARG',str(new_pos_even),service='mcsus', wait=True)


    else:
        print('You are not allowed to open the bars anymore or you got a slit there!')
        print(' ')

# Setup the name of the new mask:

mask_name0 = get('MASKNAME',service='mcsus',mode=str)
print(mask_name0)
mask_name = mask_name0.rstrip().replace(" (align)", "")


print('Current mask',mask_name)
current_mask = set('SETUPNAME',mask_name + '_wide', service='mcsus')


# Setup the CSU mask with wider alignment boxes
print('Setup the new alignment mask with wider alignment boxes')

set('CSUSETUP', 1)
print('Setting up CSU')

# Check that the status of the CSU is set up:


csu_setup_state=get('CSUREADY', service='mcsus',mode=float)
print('CSU state: ',csu_setup_state)

# If the CSU is setup (= 2), then open the alignment boxes 5 arcsec:
waitfor_CSU()
csu_setup_state=get('CSUREADY', service='mcsus',mode=float)
print('CSU state: ',csu_setup_state)

if csu_setup_state==2: #(checkout that this state is =2)

    print('Open the alignment boxes 5 arcsec')
#subprocess.Popen('modify -s mosfire csugo=1', shell=True, stdout=subprocess.PIPE).stdout
    execute_mask()
    waitfor_CSU()

    print('Alignment boxes have been open by 5 arcsec, take an image to see if you find your alignment stars')
