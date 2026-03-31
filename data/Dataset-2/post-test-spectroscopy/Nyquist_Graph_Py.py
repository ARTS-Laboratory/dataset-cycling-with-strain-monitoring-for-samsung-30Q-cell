# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:26:33 2026

@author: Charlie Buren
CHANGE ONLY excel_file_path
I may one day put this in a GUI but untill then change only excel_file_path
"""


''' Libary Setup '''
import pandas as pd
import matplotlib.pyplot as plt


''' Excel File '''
excel_file_path = 'C:/School/Navy/Data/Python/Bode/Test Data/ParallelTestBed_3_23_26_Nyquist.xlsx'
excel_file = pd.ExcelFile(excel_file_path)


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
    List_Sheet_Selection = input('Enter Nyquist Sheet: ')
    
    #Select the sheet
    Sheet_Name, Sheet_Selection, Toggle_Overlay, Choose_Color = User_Sheet_Selection(List_Sheet_Selection)

    #Drift y/n
    Drift_Toggle_Input = input("Do you want to graph the drift?\ny for yes, n for no:")
    if Drift_Toggle_Input.lower() == 'y':
        Drift_Toggle = True
    else:
        Drift_Toggle = False


    ''' Labels '''
    PlotTitle = f'{Sheet_Name} Nyquist Plot'
    Xlabel = 'Zreal (ohm)'
    Ylabel = '-Zimag (ohm)'
    
    
    ''' Nyquist Setup '''
    Zreal = Sheet_Selection['Zreal (ohm)'].values
    DriftZreal = Sheet_Selection['Zreal (ohm).1'].values
    Zimag = Sheet_Selection[' -Zimag (ohm)'].values
    DriftZimag = Sheet_Selection[' -Zimag (ohm).1'].values
    
    ''' Graphing '''
    fig, ax = plt.subplots()
    fig.suptitle(PlotTitle)
    ax.grid(True, alpha = .3)
    
    if Toggle_Overlay == False:
        ax.plot(Zreal, Zimag, color = Choose_Color, linestyle = '-', label = f'{Sheet_Name}')
        ax.set_ylabel(Ylabel)
        ax.set_xlabel(Xlabel)
        ax.legend()
    
    #Overlay
    if Toggle_Overlay == True:
        #Variables
        Zreal2 = Sheet_Selection['Zreal (ohm).2'].values
        Zreal3 = Sheet_Selection['Zreal (ohm).4'].values
        Zimag2 = Sheet_Selection[' -Zimag (ohm).2'].values
        Zimag3 = Sheet_Selection[' -Zimag (ohm).4'].values

        ax.set_ylabel(Ylabel)
        ax.plot(Zreal, Zimag, color = 'blue', linestyle = '-', label = 'Cell 1 Magnitude')
        ax.plot(Zreal2, Zimag2, color = 'red', linestyle = '-', label = 'Cell 2 Magnitude')
        ax.plot(Zreal3, Zimag3, color = 'green', linestyle = '-', label = 'Cell 3 Magnitude')
        ax.legend()
        
        
    #Drift
    if Drift_Toggle == True:
        ax.plot(DriftZreal, DriftZimag, color = 'black', linestyle = '--', label = f'{Sheet_Name} Drift')
        
        
    ''' Looping '''
    user_contin = input('Do you want to continue?\ny for Yes\nn for No: ')
    if user_contin.lower() in {'y','yes','ye'}:
        contin == True
    else:
        contin = False

''' Testing '''
#print(Sheet_Selection)
#print(Sheet_Name)
    
    