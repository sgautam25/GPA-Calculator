import tkinter as Tk
import pandas as pd
import numpy as np
import re
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import END
from io import BytesIO
import requests

data = pd.read_csv(r"C:\Users\samee\Desktop\AdmitKard\GPA_with_Tier.csv")
data.head()

options = data["School name"].to_list()

data = data.dropna()

data.isnull().sum()

def revisedGPA(list_,max_gpa): #for conversion of original list to corresponding max GPA list
    factor = float(max_gpa)/list_[0]
    r_list_ = []
    for i in list_:
        r_list_.append(i*factor)
    return r_list_

def callCalculator(gpa,sc_name,tier,percentage, max_gpa): 
    if ( gpa >= float(max_gpa) ):
        return 4 
    if(percentage == 'Percentage'): 
        gpa = gpa/10
        max_gpa = float(max_gpa)/10
    school = data.loc[data['School name'] == sc_name] #statement to search if school is present or not
    if (len(school)): #checking if school is present
            Intl_GPA = school['Intl GPA'].iloc[0].split('/')
            Intl_GPA = [float(x) for x in Intl_GPA]
            Intl_GPA.append(0)
            
            Intl_GPA = revisedGPA(Intl_GPA,max_gpa) #for the new gpa list
            x = np.array(Intl_GPA).reshape(len(Intl_GPA),1)
            US_GPA = school['US GPA'].iloc[0].split('/')
            US_GPA = [float(x) for x in US_GPA]
            US_GPA.append(0)
            #US_GPA = Addmax(US_GPA,max_gpa)
            
            #type(US_GPA[0])
            #y = np.array(US_GPA).reshape(len(US_GPA),1)
    else:
            college_tier = data.loc[data['Tier'] == tier]
            Intl_GPA = []
            for i in range(len(college_tier)): 
                Intl = college_tier['Intl GPA'].iloc[i].split('/')
                Intl = [float(x) for x in Intl]
                Intl.append(0)
                #x = np.array(Intl_GPA).reshape(len(Intl_GPA),1)
                US = college_tier['US GPA'].iloc[i].split('/')
                US = [float(x) for x in US]
                US.append(0)
                if(len(Intl) > len(Intl_GPA)):
                    Intl_GPA = Intl
                    US_GPA = US
            Intl_GPA = revisedGPA(Intl_GPA,max_gpa) 
            
   #Calculator function                 
    i = len(Intl_GPA)-1
    while(i >= 0):
        if Intl_GPA[i]<=gpa:
            i-=1
            continue
        else: 
            break
    if(i < 0):
        indx = 0
    else:
        indx = i
           
#Equation of line
#Slope
    m = (US_GPA[i] - US_GPA[i+1])/(Intl_GPA[i] - Intl_GPA[i+1])
            #Intersect
    c = US_GPA[i] - m*Intl_GPA[i]
    predict = m*gpa + c
    if(predict > 4):
        return 4
    return predict


from tkinter import *
from tkinter import ttk
import tkinter.messagebox

window=Tk()
window.title('GPA Calculator')
window.config() 
window.geometry('500x600')

new_colleges = []
def clear_frame():
    for widgets in frame.winfo_children():
        widgets.destroy()
    
def checkTier(sc_name):
    clear_frame()
    if(len(data.loc[data['School name'] == sc_name.get()]) == 0):
        tkinter.messagebox.showinfo("Instruction",  "Please select tier")
        tier = createBox("Tier", list(data["Tier"].unique()),frame)
        Label(frame, text="*Instructions : Please note that this will calculate the relative CGPA as per the California University cgpa calculation system !! ", font=('Calibri 8')).pack()
        Label(frame, text=" If your college comes under Tier III, please select respective option ", font=('Calibri 8')).pack()
        new_colleges.append(sc_name.get())
    else:
        tier = "None"
    percentage = createBox("Percentage/CGPA", ['Percentage','CGPA'],frame)
    Label(frame, text="*Instructions : If your college calculates grades in percentage then choose 'Percentage' option ", font=('Calibri 8')).pack()
    
    Label(frame, text="Max GPA/Percentage", font=('Calibri 14')).pack()
    Label(frame, text="*Instructions: For eg: 10 (if your college calculates grades with respect to '10' ), enter '10' ", font=('Calibri 8')).pack()
    max_gpa=Entry(frame, width=35)
    max_gpa.pack()
    
    Label(frame, text="Enter GPA/Percentage", font=('Calibri 10')).pack()
    gpa=Entry(frame, width=35)
    gpa.pack()
    output=Label(frame, font=('Calibri 15'))
    Button(frame, text="Calculate", command= lambda : getUSgpa(gpa,output,tier,percentage,max_gpa)).pack()

def getUSgpa(gpa,output,tier,percentage,max_gpa):
    gpa_get = float(gpa.get())
    if(tier == "None"):
        us_gpa = callCalculator(gpa_get,sc_name.get(),tier,percentage.get(),max_gpa.get())
    else:
        us_gpa = callCalculator(gpa_get,sc_name.get(),tier.get(),percentage.get(),max_gpa.get())
    output.config(text=us_gpa)
    output.pack(pady=20)
     #Label(window, text=f'{us_gpa}', pady=20, bg='#ffbf00').pack()

def createBox(txt, values,win):
    label = Label(win, text=txt)
    label.config(font=("Courier",15))
    label.pack()
    entry = AutocompleteCombobox(win, width=70, completevalues=values )
    entry.pack()
    return entry

sc_name = createBox("School/University Name", data["School name"].to_list(),window)
Label(window, text="*Instructions : If your college is not listed above, press Enter!", font=('Calibri 8')).pack()
Button(window,text = "Enter",command= lambda : checkTier(sc_name)).pack()
frame = Frame(window)
frame.pack(side="top", expand=True, fill="both")

window.mainloop()
print(new_colleges)

new_colleges