# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 11:24:36 2026

@author: Charlie Buren
CHANGE ONLY excel_file_path
I may one day put this in a GUI but untill then change only excel_file_path
"""


''' Libary Setup '''
#import os
import pandas as pd
import matplotlib.pyplot as plt


''' Update These Paths '''
excel_file_path = 'C:/School/Navy/Data/Python/Bode/Test Data/Rack3_3_24_26_Bode.xlsx'
media_file_path = 'C:/School/Navy/Data/Python/Media'

''' File Paths '''
excel_file = pd.ExcelFile(excel_file_path)
#media_file = os.path.abspath


def User_Sheet_Selection(Sheet_Cell_Name):
    match Sheet_Cell_Name:
        case 'Cell 1':
            Sheet_Name = List_Sheet[0]
            Sheet_Selection = pd.read_excel(excel_file, Sheet_Name, header = 1)
            Toggle_Overlay = False
            Choose_Color = 'blue'
        case 'Cell 2':
            Sheet_Name = List_Sheet[1]
            Sheet_Selection = pd.read_excel(excel_file, Sheet_Name, header = 1)
            Toggle_Overlay = False
            Choose_Color = 'red'
        case 'Cell 3':
            Sheet_Name = List_Sheet[2]
            Sheet_Selection = pd.read_excel(excel_file, Sheet_Name, header = 1)
            Toggle_Overlay = False
            Choose_Color = 'green'
        case 'Overlay':
            Sheet_Name = List_Sheet[3]
            Sheet_Selection = pd.read_excel(excel_file, Sheet_Name, header = 1)
            Toggle_Overlay = True
            Choose_Color = 'blue'
        case _:
            print('Error')
    return Sheet_Name, Sheet_Selection, Toggle_Overlay, Choose_Color



''' Sheet Setup'''
List_Sheet = ['Cell 1', 'Cell 2', 'Cell 3', 'Overlay']

contin = True
while contin == True:
    List_Sheet_Selection = input('Enter Bode Sheet: ')
    
    #Select the sheet
    Sheet_Name, Sheet_Selection, Toggle_Overlay, Choose_Color = User_Sheet_Selection(List_Sheet_Selection)

    #Drift y/n
    Drift_Toggle_Input = input("Do you want to graph the drift?\ny for yes, n for no:")
    if Drift_Toggle_Input.lower() == 'y':
        Drift_Toggle = True
    else:
        Drift_Toggle = False


    ''' Labels '''
    PlotTitle = f'{Sheet_Name} Bode Plot'
    Ylabel_Mag = 'Mod (ohm)'
    Ylabel_Phase = 'Zphz (deg)'
    Xlabel_Phase = 'Frequency (Hz)'


    ''' Bode Setup '''
    Freq = Sheet_Selection['Freq (Hz)'].values 
    DriftFreq = Sheet_Selection['Freq (Hz).1'].values  
    Zmod = Sheet_Selection['Zmod (ohm)'].values 
    DriftZmod = Sheet_Selection['Zmod (ohm).1'].values 
    Zphz = Sheet_Selection['Zphz (deg)'].values 
    DriftZphz = Sheet_Selection['Zphz (deg).1'].values 


    ''' Graphing '''
    Bode_Plot = plt.figure(layout="constrained")
    Plot_Array = Bode_Plot.subplots(2,1, squeeze = False)
    Bode_Plot.suptitle(PlotTitle)
    
    if Toggle_Overlay == False:
        #Mag Graph (Top)
        Bode_Mag_Plot = Plot_Array[0,0]
        Bode_Mag_Plot.semilogx(Freq, Zmod, color = Choose_Color, linestyle = '-', label = f'{Sheet_Name} Magnitude') #semilogx is for graphing logs
        Bode_Mag_Plot.set_ylabel(Ylabel_Mag)
        Bode_Mag_Plot.legend()
    
        #Phase Graph (Bot)
        Bode_Phase_Plot = Plot_Array[1,0]
        Bode_Phase_Plot.semilogx(Freq, Zphz, color = Choose_Color, linestyle = '-', label = f'{Sheet_Name} Phase') #semilogx is for graphing logs
        Bode_Phase_Plot.set_ylabel(Ylabel_Phase)
        Bode_Phase_Plot.set_xlabel(Xlabel_Phase)
        Bode_Phase_Plot.legend()
    
    #Overlay
    if Toggle_Overlay == True:
        #Variables
        Freq2 = Sheet_Selection['Freq (Hz).2'].values
        DriftFreq2 = Sheet_Selection['Freq (Hz).3'].values  
        Freq3 = Sheet_Selection['Freq (Hz).4'].values
        DriftFreq3 = Sheet_Selection['Freq (Hz).5'].values
        Zmod2 = Sheet_Selection['Zmod (ohm).2'].values
        DriftZmod2 = Sheet_Selection['Zmod (ohm).3'].values
        Zmod3 = Sheet_Selection['Zmod (ohm).4'].values
        DriftZmod3 = Sheet_Selection['Zmod (ohm).5'].values
        Zphz2 = Sheet_Selection['Zphz (deg).2'].values
        DriftZphz2 = Sheet_Selection['Zphz (deg).3'].values
        Zphz3 = Sheet_Selection['Zphz (deg).4'].values
        DriftZphz3 = Sheet_Selection['Zphz (deg).5'].values
        
        #Mag Graph (Top)
        Bode_Mag_Plot = Plot_Array[0,0]
        Bode_Mag_Plot.set_ylabel(Ylabel_Mag)
        Bode_Mag_Plot.semilogx(Freq, Zmod, color = 'blue', linestyle = '-', label = 'Cell 1 Magnitude')
        Bode_Mag_Plot.semilogx(Freq2, Zmod2, color = 'red', linestyle = '-', label = 'Cell 2 Magnitude')
        Bode_Mag_Plot.semilogx(Freq3, Zmod3, color = 'green', linestyle = '-', label = 'Cell 3 Magnitude')
        Bode_Mag_Plot.legend()
        
        #Phase Graph (Bot)
        Bode_Phase_Plot = Plot_Array[1,0]
        Bode_Phase_Plot.set_ylabel(Ylabel_Phase)
        Bode_Phase_Plot.set_xlabel(Xlabel_Phase)
        Bode_Phase_Plot.semilogx(Freq, Zphz, color = 'blue', linestyle = '-', label = 'Cell 1 Phase')
        Bode_Phase_Plot.semilogx(Freq2, Zphz2, color = 'red', linestyle = '-', label = 'Cell 2 Phase')
        Bode_Phase_Plot.semilogx(Freq3, Zphz3, color = 'green', linestyle = '-', label = 'Cell 3 Phase')
        Bode_Phase_Plot.legend()
        
        #Drift
        if Drift_Toggle == True:
            Bode_Mag_Plot.semilogx(DriftFreq2, DriftZmod2, color = 'black', linestyle = '--', label = f'{Sheet_Name} Drift Magnitude')
            Bode_Phase_Plot.semilogx(DriftFreq2, DriftZphz2, color = 'black', linestyle = '--', label = f'{Sheet_Name} Drift Phase')
            Bode_Mag_Plot.semilogx(DriftFreq3, DriftZmod3, color = 'black', linestyle = '--', label = f'{Sheet_Name} Drift Magnitude')
            Bode_Phase_Plot.semilogx(DriftFreq3, DriftZphz3, color = 'black', linestyle = '--', label = f'{Sheet_Name} Drift Phase')
            Bode_Phase_Plot.legend()
        
    #Drift
    if Drift_Toggle == True:
        Bode_Mag_Plot.semilogx(DriftFreq, DriftZmod, color = 'black', linestyle = '--', label = f'{Sheet_Name} Drift Magnitude')
        Bode_Phase_Plot.semilogx(DriftFreq, DriftZphz, color = 'black', linestyle = '--', label = f'{Sheet_Name} Drift Phase')
        
        
    ''' Looping '''
    user_contin = input('Do you want to continue?\ny for Yes\nn for No: ')
    if user_contin.lower() in {'y','yes','ye'}:
        contin == True
    else:
        contin = False

''' Testing '''
#print(Sheet_Selection)
#print(Sheet_Name)




