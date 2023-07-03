# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 15:30:45 2021

@author: cyang58
"""

import time
from HFSS import HFSS
start_time = time.time()

h = HFSS()

# Launch ANSYS Electronics Desktop
h.launch()
print('Successfully open ANSYS Electronics Desktop')
#
# Set all variables
h.init()
h.setVariable('Patch_length', 7.15, 'mm')
h.setVariable('Patch_width', 9.94, 'mm')
h.setVariable('Array_space_x', 15, 'mm')
h.setVariable('Array_space_y', 15, 'mm')
h.setVariable('Substrate_height', 0.813, 'mm')
h.setVariable('Feed_inner_radius', 0.635, 'mm')
h.setVariable('Feed_offset', 1.75, 'mm')
h.setVariable('Feed_height', 9, 'mm')
h.setVariable('M', 5, '') # Row number of array
h.setVariable('N', 5, '') # Column number of array
print('Successfully Set all variables')
Row_num=int(h.getVariablevalue('M'))
Column_num=int(h.getVariablevalue('N'))
Array_space_x=h.getVariablevalue('Array_space_x')
Array_space_x_value,Array_space_unit=h.convertVariabletovalueandunit(Array_space_x)
Array_space_y=h.getVariablevalue('Array_space_y')
Array_space_y_value,Array_space_unit=h.convertVariabletovalueandunit(Array_space_y)
# Set up an array model with M*N Retangular Grid
for i in range(0,Row_num):
    for j in range(0,Column_num):
        #set up i th row and j th column antenna element 
        Element_position_x=(j-(Column_num-1)/2)*Array_space_x_value
        Element_position_y=((Row_num-1)/2-i)*Array_space_y_value
        h.createBox('-Array_space_x/2+'+str(Element_position_x)+Array_space_unit,'-Array_space_y/2+'+str(Element_position_y)+Array_space_unit,'-Substrate_height', 'Array_space_x','Array_space_y','Substrate_height','Subsrate'+str(j+i*Column_num), 'Rogers RO4003 (tm)','')
        h.createRectangle('-Patch_width/2+'+str(Element_position_x)+Array_space_unit,'-Patch_length/2+'+str(Element_position_y)+Array_space_unit,'0mm','Patch_width','Patch_length','Z', 'Patch'+str(j+i*Column_num))
        h.assignPerfectE('Patch'+str(j+i*Column_num),'PEC'+str(j+i*Column_num))
        h.createRectangle('-Array_space_x/2+'+str(Element_position_x)+Array_space_unit,'-Array_space_y/2+'+str(Element_position_y)+Array_space_unit,'-Substrate_height','Array_space_x','Array_space_y','Z', 'Ground'+str(j+i*Column_num))
        h.createCircle(str(Element_position_x)+Array_space_unit,str(Element_position_y)+Array_space_unit+'-Feed_offset','-Substrate_height','2.03mm','Z','Ground_hole'+str(j+i*Column_num))
        h.subtractf('Ground'+str(j+i*Column_num),'Ground_hole'+str(j+i*Column_num))
        h.assignPerfectE('Ground'+str(j+i*Column_num),'PEC_ground'+str(j+i*Column_num))
        h.createCylinder(str(Element_position_x)+Array_space_unit,str(Element_position_y)+Array_space_unit+'-Feed_offset','-Substrate_height','2.03mm','-Feed_height','Z','Feed_substrate'+str(j+i*Column_num),'teflon_based','')
        h.createCylinder(str(Element_position_x)+Array_space_unit,str(Element_position_y)+Array_space_unit+'-Feed_offset','-Substrate_height','2.8mm','-Feed_height','Z','Feed_outer'+str(j+i*Column_num),'copper','F')
        h.createCylinder(str(Element_position_x)+Array_space_unit,str(Element_position_y)+Array_space_unit+'-Feed_offset','0mm','Feed_inner_radius','-Feed_height-Substrate_height','Z','Feed_inner'+str(j+i*Column_num),'copper','F')
        h.createCylinder(str(Element_position_x)+Array_space_unit,str(Element_position_y)+Array_space_unit+'-Feed_offset','-Feed_height-Substrate_height','2.8mm','-2mm','Z','Port_element'+str(j+i*Column_num),'pec','F')
        h.subtractt('Feed_outer'+str(j+i*Column_num),'Feed_substrate'+str(j+i*Column_num))
        h.subtractt('Feed_substrate'+str(j+i*Column_num),'Feed_inner'+str(j+i*Column_num))
        h.subtractt('Subsrate'+str(j+i*Column_num),'Feed_inner'+str(j+i*Column_num))
        face_id = h.getFacebyposition('Port_element'+str(j+i*Column_num),str(Element_position_x)+Array_space_unit,str(Element_position_y)+Array_space_unit+'-Feed_offset','-Feed_height-Substrate_height')
        Feed_of=h.getVariablevalue('Feed_offset')
        Feed_of_value,Feed_of_unit=h.convertVariabletovalueandunit(Feed_of)
        Feed_he=h.getVariablevalue('Feed_height')
        Feed_he_value,Feed_he_unit=h.convertVariabletovalueandunit(Feed_he)
        Substrate_he=h.getVariablevalue('Substrate_height')
        Substrate_he_value,Substrate_he_unit=h.convertVariabletovalueandunit(Substrate_he)    
        h.assignWaveportwithname('Port'+str(j+i*Column_num),face_id,str(Element_position_x)+Array_space_unit,str(Element_position_y-Feed_of_value)+Feed_of_unit,'-'+str(Feed_he_value+Substrate_he_value)+Substrate_he_unit,str(Element_position_x-2.8)+Array_space_unit,str(Element_position_y-Feed_of_value)+Feed_of_unit,'-'+str(Feed_he_value+Substrate_he_value)+Substrate_he_unit)        
        h.fitAll()
# Set Exciation and radiation boundary
h.createRegion('30mm')
h.assignRadiationRegion()
print('Successfully set Model, exciation and radiation boundary')

# Set setup and analysis and solve
h.insertSetup('Setup1', '10GHz')
h.insertFrequencysweep('Setup1', '9GHz', '11GHz', '50MHz', 'Fast')
h.fitAll()
h.saveProject()
#h.solve('Setup1')


'''
#%% Set setup PSO and start optimization
from PSO import PSO
def demo_func(x):
     DR_sidelength, DR_height, InDR_sidelength, InDR_height, Monopole_position, Monopole_height = x
     return

pso = PSO(func=demo_func, n_dim=6, pop=30, max_iter=25, lb=[20, 10, 1, 1, 5, 6], ub=[35, 45, 20, 35, 25, 15], w=0.8, c1=0.5, c2=0.5)
pso.run() 
#h.saveProject()
#h.solve('Setup1')
#h.createSpreport('Sparameter','Setup1'))
#h.exportTofile('Sparameter', result_path, Filename)

# Optimization over and close the software
'''
#h.closeProject()
print('Successfully Slove and export the result')
