# -*- coding: utf-8 -*-
"""
Created on Tue May 30 17:20:50 2023

@author: chenyang
"""

from win32com import client
oAnsoftApp = client.Dispatch('AnsoftHfss.HfssScriptInterface')
oDesktop = oAnsoftApp.GetAppDesktop()
oDesktop.RestoreWindow()
oProject = oDesktop.NewProject()
oProject.InsertDesign('HFSS', 'HFSSDesign1', 'DrivenModal1', '')
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oModule = oDesign.GetModule('BoundarySetup')
transparency = 0.

#%%
oDesktop = oAnsoftApp.GetAppDesktop()
oDesktop.QuitApplication()
