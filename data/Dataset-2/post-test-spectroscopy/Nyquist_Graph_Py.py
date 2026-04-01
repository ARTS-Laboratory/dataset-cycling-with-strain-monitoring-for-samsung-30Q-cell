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


''' Update These Paths '''
excel_file_path = 'C:/School/Navy/Github/dataset-cycling-with-strain-monitoring-for-samsung-30Q-cell/data/Dataset-2/post-test-spectroscopy/Excel/Test_Nyquist.xlsx'
media_file_path = 'C:/School/Navy/Github/dataset-cycling-with-strain-monitoring-for-samsung-30Q-cell/data/Dataset-2/post-test-spectroscopy/Media'
save_type = '.png' #what file type graph will be saved as


''' Excel File Path '''
excel_file = pd.ExcelFile(excel_file_path)
List_Sheet_Selection = 'Cell 1'


def User_Sheet_Selection(Sheet_Cell_Name):
    match Sheet_Cell_Name:
        case 'Cell 1':
            Sheet_Name = List_Sheet[0]
            Sheet_Selection = pd.read_excel(excel_file, Sheet_Name, header = 1)
            Toggle_Overlay = False
            Choose_Color = 'blue'
            List_Sheet_Selection = 'Cell 2'
            contin = True
        case 'Cell 2':
            Sheet_Name = List_Sheet[1]
            Sheet_Selection = pd.read_excel(excel_file, Sheet_Name, header = 1)
            Toggle_Overlay = False
            Choose_Color = 'red'
            List_Sheet_Selection = 'Cell 3'
            contin = True
        case 'Cell 3':
            Sheet_Name = List_Sheet[2]
            Sheet_Selection = pd.read_excel(excel_file, Sheet_Name, header = 1)
            Toggle_Overlay = False
            Choose_Color = 'green'
            List_Sheet_Selection = 'Overlay'
            contin = True
        case 'Overlay':
            Sheet_Name = List_Sheet[3]
            Sheet_Selection = pd.read_excel(excel_file, Sheet_Name, header = 1)
            Toggle_Overlay = True
            Choose_Color = 'blue'
            List_Sheet_Selection = 'Cell 1'
            contin = False
        case _:
            print('Error')
    return Sheet_Name, Sheet_Selection, Toggle_Overlay, Choose_Color, List_Sheet_Selection, contin


''' Sheet Setup'''
List_Sheet = ['Cell 1', 'Cell 2', 'Cell 3', 'Overlay']

#Drift y/n
Drift_Toggle_Input = input("Do you want to graph the drift?\ny for yes, n for no:")
if Drift_Toggle_Input.lower() == 'y':
    Drift_Toggle = True
else:
    Drift_Toggle = False
        
contin = True
while contin == True:    
    #Select the sheet
    Sheet_Name, Sheet_Selection, Toggle_Overlay, Choose_Color, List_Sheet_Selection, contin = User_Sheet_Selection(List_Sheet_Selection)


    ''' Labels '''
    PlotTitle = f'{Sheet_Name} Nyquist Plot'
    Xlabel = 'Zreal (ohm)'
    Ylabel = '-Zimag (ohm)'
    
    ''' Media Setup '''
    File_Title_Path = PlotTitle.replace(' ','_')
    if Drift_Toggle == True:
        File_Title = f'{File_Title_Path}_Drift{save_type}'
    else:
        File_Title = f'{File_Title_Path}{save_type}'
    save_media_path = f'{media_file_path}/{File_Title}'
    
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
        DriftZreal2 = Sheet_Selection['Zreal (ohm).3'].values
        Zreal3 = Sheet_Selection['Zreal (ohm).4'].values
        DriftZreal3 = Sheet_Selection['Zreal (ohm).5'].values
        Zimag2 = Sheet_Selection[' -Zimag (ohm).2'].values
        DriftZimag2 = Sheet_Selection[' -Zimag (ohm).3'].values
        Zimag3 = Sheet_Selection[' -Zimag (ohm).4'].values
        DriftZimag3 = Sheet_Selection[' -Zimag (ohm).5'].values

        ax.set_ylabel(Ylabel)
        ax.plot(Zreal, Zimag, color = 'blue', linestyle = '-', label = 'Cell 1 Magnitude')
        ax.plot(Zreal2, Zimag2, color = 'red', linestyle = '-', label = 'Cell 2 Magnitude')
        ax.plot(Zreal3, Zimag3, color = 'green', linestyle = '-', label = 'Cell 3 Magnitude')
        ax.legend()
        
        if Drift_Toggle == True:
            ax.plot(DriftZreal2, DriftZimag2, color = 'black', linestyle = '--', label = f'{Sheet_Name} Drift')
            ax.plot(DriftZreal3, DriftZimag3, color = 'black', linestyle = '--', label = f'{Sheet_Name} Drift')
        
        #Save Graph
        fig.savefig(save_media_path)
        
    #Drift
    if Drift_Toggle == True:
        ax.plot(DriftZreal, DriftZimag, color = 'black', linestyle = '--', label = f'{Sheet_Name} Drift')
    
    #Save Graph
    fig.savefig(save_media_path)

''' Testing '''
#print(Sheet_Selection)
#print(Sheet_Name)
    
    