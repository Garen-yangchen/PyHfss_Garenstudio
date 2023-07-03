# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 11:04:00 2022

This program is writing for Ansys HFSS software. It possesses three parts including the basic software operations, 
advanced data post-process, and optimization algorithms. Maybe it will also have some GUI design and others.

The program starts from 18th NOV. 2020 at City University of HK. Here we have a group of partners, Hope we can complete 
this huge project. Best regards to us.

@author: cyang58
"""
import time
import numpy as np
#import math as mt
import re
import math as mt
from HFSS import HFSS

start_time = time.time()


h = HFSS()
# result_path = r'C:\Users\YANG Chen\Desktop\Python for HFSS\Result'
# Filename='S Parameter.csv'

# Launch ANSYS Electronics Desktop
h.launch()
print('Successfully open ANSYS Electronics Desktop')

# Set all variables
M=4
N=4
h.setVariable('Ground_length', 140, 'mm')
h.setVariable('Ground_thickness', 2, 'mm')
h.setVariable('M', M, '')
h.setVariable('N', N, '')
h.setVariable('Element_space', 27, 'mm')
h.setVariable('Feed_offset', 0, 'mm')
h.setVariable('DR_length', 13.5, 'mm')
h.setVariable('DR_width', 13.5, 'mm')
h.setVariable('DR_height', 30, 'mm')
h.setVariable('Probe_radius', 0.635, 'mm')
h.setVariable('Probe_height', 9.2, 'mm')
h.setVariable('Feed_height', 5, 'mm')
#h.setVariable('Field_boundary', 'DR_sidelength/2', '')
print('Successfully Set all variables')

# Set model
h.createBox('-Ground_length/2','-Ground_length/2','-Ground_thickness', 'Ground_length','Ground_length','Ground_thickness','Ground', 'Copper','F')
h.fitAll()
h.addMaterial('DK7', 7, 0.0032)
h.createBox('-DR_width/2','-DR_length/2','0 mm', 'DR_width','DR_length','DR_height','DR', 'DK7','')
h.move('DR', '-(M-1)/2*Element_space','-(N-1)/2*Element_space', '0 mm' )
h.duplicateMove('DR', 'Element_space','0 mm', '0 mm', 'M', '')
h.duplicateMove('DR', '0mm','Element_space', '0 mm', 'N', '')

h.createCylinder('DR_width/2+Probe_radius','Feed_offset','-Feed_height','Probe_radius','Feed_height+Probe_height','Z','Feed_Probe', 'Copper', 'F')
h.move('Feed_Probe', '-(M-1)/2*Element_space','-(N-1)/2*Element_space', '0 mm' )
h.duplicateMove('Feed_Probe', 'Element_space','0 mm', '0 mm', 'M', '')
h.duplicateMove('Feed_Probe', '0mm','Element_space', '0 mm', 'N', '')

h.createCylinder('DR_width/2+Probe_radius','Feed_offset','-Ground_thickness','2.03 mm','Ground_thickness','Z','Ground_hole', 'Copper', 'F')
h.move('Ground_hole', '-(M-1)/2*Element_space','-(N-1)/2*Element_space', '0 mm' )
h.duplicateMove('Ground_hole', 'Element_space','0 mm', '0 mm', 'M', '')
h.duplicateMove('Ground_hole', '0mm','Element_space', '0 mm', 'N', '')

h.createCylinder('DR_width/2+Probe_radius','Feed_offset','-Feed_height','2.03 mm','Feed_height','Z','Feed_substrate', 'Teflon (tm)', '')
h.move('Feed_substrate', '-(M-1)/2*Element_space','-(N-1)/2*Element_space', '0 mm' )
h.duplicateMove('Feed_substrate', 'Element_space','0 mm', '0 mm', 'M', '')
h.duplicateMove('Feed_substrate', '0mm','Element_space', '0 mm', 'N', '')

h.createCylinder('DR_width/2+Probe_radius','Feed_offset','-Feed_height','2.2 mm','Feed_height-Ground_thickness','Z','Feed_outer', 'Copper', 'F')
h.move('Feed_outer', '-(M-1)/2*Element_space','-(N-1)/2*Element_space', '0 mm' )
h.duplicateMove('Feed_outer', 'Element_space','0 mm', '0 mm', 'M', '')
h.duplicateMove('Feed_outer', '0mm','Element_space', '0 mm', 'N', '')

h.subtractt('Feed_outer','Feed_substrate')
h.subtractt('Feed_substrate','Feed_Probe')
h.subtractt('Ground','Ground_hole')

# Set Exciation and radiation boundary
h.createCylinder('DR_width/2+Probe_radius','Feed_offset','-Feed_height','2.2 mm','-3 mm','Z','Feed_Port', 'PEC', 'F')
face_id=h.getFacebyposition('Feed_Port', 'DR_width/2', 'Feed_offset', '-Feed_height')
h.assignsimplyWaveport(face_id)
h.move('Feed_Port', '-(M-1)/2*Element_space','-(N-1)/2*Element_space', '0 mm' )
h.duplicateMove('Feed_Port', 'Element_space','0 mm', '0 mm', 'M', 'T')
h.duplicateMove('Feed_Port', '0mm','Element_space', '0 mm', '2', 'T')
h.duplicateMove('Feed_Port_4', 'Element_space','0 mm', '0 mm', 'M', 'T')
h.duplicateMove('Feed_Port_4', '0mm','Element_space', '0 mm', '2', 'T')
h.duplicateMove('Feed_Port_4_4', 'Element_space','0 mm', '0 mm', 'M', 'T')
h.duplicateMove('Feed_Port_4_4', '0mm','Element_space', '0 mm', '2', 'T')
h.duplicateMove('Feed_Port_4_4_4', 'Element_space','0 mm', '0 mm', 'M', 'T')
h.createRegion('40mm')
h.assignRadiationRegion()
print('Successfully set Model, exciation and radiation boundary')
#%%
# Set setup and analysis and solve
h.insertSetup('Setup1', '4.9GHz')
h.insertFrequencysweep('Setup1', '3.5GHz', '6.5GHz', '150MHz', 'Discrete')
h.saveProject()
h.solve('Setup1')

####################################
# Export the field results
####################################





print('Finished all!')
