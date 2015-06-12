# -*- coding: utf-8 -*-  
from Tkinter import *
import tkMessageBox
import math

COEF_1_LBS_TO_KG = 0.45359237 # 1 lbs = 0.45359237 kg
HR_TO_SEC = 3600 # 1 hr = 3600 s

items_wait4calc = {} # use dicts to add functions to the add button

read_success = False
button_number = 0

#exist_air = False
#exist_steam = False
#exist_other_g = False
#equivalent_all = 0

# 以下字典后期将与数据库连接，通过数据库进行存储、读取、修改等操作
mole_weight = {}  

class Gas_item:

    def __init__(self, g_name, g_mass, g_unit_m, g_temperature, g_unit_t):

        self.name = g_name
        self.m = g_mass
        self.m_is_iu = g_unit_m
        self.t = g_temperature
        self.t_is_iu = g_unit_t

    def __str__(self):

        string_0 = "Gas name: " + self.name + "\n"

        if self.m_is_iu:
            mass_unit = " kg/s"
        else:
            mass_unit = " lbs/hr"
        string_1 = "Mass: " + str(self.m) + mass_unit + "\n"
  
        if self.t_is_iu:
            temp_unit = " degree C"
        else:
            temp_unit = " degree F"
        string_2 = "Temperature: " + str(self.t) + temp_unit + "\n"

        return string_0 + string_1 + string_2

class App:

    def __init__(self, master):

        self.frame = Frame(master)
        self.frame.pack()

        self.read_data_btn = Button(self.frame, text = "Read", command = self.read_data)
        self.read_data_btn.pack(side = LEFT)

        
    def read_data(self):
    
        global read_success
        
        try:
            readf = open('MoleWT_data.txt', 'r')

            sum_items = int(readf.readline())

            for index in range(0, sum_items):
                temp_readl = readf.readline()
                j = 0
                key_name = ''
                key_value = ''
                while (temp_readl[j] != ' '):
                    key_name += temp_readl[j]
                    j += 1
                j += 1
                while (temp_readl[j] != '\n'):
                    key_value += temp_readl[j]
                    j += 1
                mole_weight[key_name] = float(key_value)

            readf.close()
            tkMessageBox.showinfo("Succeed!", "Reading finished!")
            self.read_data_btn.destroy()
            
            self.add_items_btn = Button(self.frame, text="Add/Modify/Delete", command=self.add_items)
            self.add_items_btn.pack(side=LEFT)
            
            # Panel 1 for Name
            m1 = PanedWindow(self.frame)
            m1.pack(fill = BOTH, expand = 1)

            label_name = Label(m1, text = "Name: ")
            m1.add(label_name)

            self.entry_name = Entry(m1)
            m1.add(self.entry_name)

            # Panel 2_1 for Mass
            m2_1 = PanedWindow(m1)
            m1.add(m2_1)

            label_mass = Label(m2_1, text = "Mass: ")
            m2_1.add(label_mass)

            self.entry_mass = Entry(m2_1)
            m2_1.add(self.entry_mass)

            # Panel 2_2 for Unit(Mass)
            m2_2 = PanedWindow(m2_1)
            m2_1.add(m2_2)   # Don't forget this sentence!!!

            self.unit_m = IntVar() # True means kg, while False means lbs  # No need to be global variable
            self.unit_m.set(0)     # have to use variable class like IntVar(). simple int can't make the radiobutton know the group
            btn_unit_m_lbs = Radiobutton(m2_2, text = "lbs/hr", variable = self.unit_m, value = 0)
            btn_unit_m_lbs.pack(anchor = W)
            btn_unit_m_kg = Radiobutton(m2_2, text = "kg/s", variable = self.unit_m, value = 1)
            btn_unit_m_kg.pack(anchor = W)

            #panel 3_1 for Temperature
            m3_1 = PanedWindow(m2_1)  # master has to be m2_1. if m2_2, label will cover the radiobutton
            m2_1.add(m3_1)  # master has to be m2_1. if m2_2, label will cover the radiobutton

            label_temperature = Label(m3_1, text = "Temperature: ")
            m3_1.add(label_temperature)

            self.entry_temperature = Entry(m3_1)
            m3_1.add(self.entry_temperature)

            # panel 3_2 for Unit(Temperature)
            m3_2 = PanedWindow(m3_1)
            m3_1.add(m3_2)

            self.unit_t = IntVar() # True means degree C, while False means degree F # No need to be global variable
            self.unit_t.set(0)     # have to use variable class like IntVar(). simple int can't make the radiobutton know the group
            btn_unit_t_F = Radiobutton(m3_2, text = "degree F", variable = self.unit_t , value = 0)
            btn_unit_t_F.pack(anchor = W)
            btn_unit_t_C = Radiobutton(m3_2, text = "degree C", variable = self.unit_t, value = 1)
            btn_unit_t_C.pack(anchor = W)
            
        except:
            tkMessageBox.showerror("ERROR", "File BROKEN or NOT EXISTENT. Read documents, then modify or create the data file.")
        
    def add_items(self):
    
        global button_number
        
        not_destroy_button = False
        
        valid_input = False # if data are all valid input, then transf2object 
        
        try:
            transf2mass = float(self.entry_mass.get())
            valid_input = True
        except:
            tkMessageBox.showerror("Type ERROR for MASS", "Input NUMBER for MASS please")
            
        try:
            transf2temp = float(self.entry_temperature.get())
        except:
            tkMessageBox.showerror("Type ERROR for TEMPERATURE", "Input NUMBER for TEMPERATURE please")
            valid_input = False
            
        if valid_input:
            object_ei = Gas_item(self.entry_name.get().lower(), transf2mass, self.unit_m.get(), transf2temp, self.unit_t.get())
        
            if not (object_ei.name in items_wait4calc.keys()):
                if (object_ei.m != 0):
                    items_wait4calc[object_ei.name] = object_ei # if not exist and the mass != 0, add this new object into the list
                elif (len(items_wait4calc) == 0):    # if no items and try to add an object with mass 0, then can't destroy the buttons
                    not_destroy_button = True
            elif (object_ei.m == 0):              # delete this object if existed and mass == 0
                items_wait4calc.pop(object_ei.name)
                if (len(items_wait4calc) == 0):         # not useful if add 0 judgement here
                    button_number = 0
            else:
                items_wait4calc[object_ei.name] = object_ei # modify the object existed
            
            if (len(items_wait4calc) != 0):
                if (button_number == 0):
                    button_number = 1
                    self.button_see_items = Button(self.frame, text="Already", command=self.see_items)
                    self.button_see_items.pack(side=LEFT)
                    self.button_clear_items = Button(self.frame, text="Clear", command=self.clear_items)
                    self.button_clear_items.pack(side=RIGHT)
                    self.button_calculation = Button(self.frame, text = "CALC", command = calculation)
                    self.button_calculation.pack(side = LEFT)
            elif not not_destroy_button:
                self.button_see_items.destroy()               # must add 0 judgement here
                self.button_clear_items.destroy()
                self.button_calculation.destroy()

    def clear_items(self):

        global items_wait4calc, button_number

        items_wait4calc = {}
        button_number = 0
        self.button_see_items.destroy()
        self.button_clear_items.destroy()
        self.button_calculation.destroy()

            
    def see_items(self):
        
        global items_wait4calc
        
        content_now = ""
        
        for i in items_wait4calc:
        
            content_now += ('Name: ' + items_wait4calc[i].name + ' Mass:' + str(items_wait4calc[i].m))
            
            if items_wait4calc[i].m_is_iu:
                content_now += ' kg'
            else:
                content_now += ' lbs'
                
            content_now += (' Temperature:' + str(items_wait4calc[i].t) + '\n')
            
            if items_wait4calc[i].t_is_iu:
                content_now += ' degree C'
            else:
                content_now += ' degree F'
                
            content_now += '\n'
            
        tkMessageBox.showinfo("Including...", content_now)
        
def calculation():

    global items_wait4calc

    exist_air = False
    exist_steam = False
    exist_other_g = False
    
    items_calc = items_wait4calc.copy()
    m_sum = 0
    n_sum = 0
    n = {}
    error_flag = False
    
    ########## step 1: data preprocessing ##########
    
    for i in items_calc:
    
        if ("steam" == items_calc[i].name):            # step 1.1 : judge if air/steam/other gas
            exist_steam = True
        elif ("air" == items_calc[i].name):
            exist_air = True
        else:
            exist_other_g = True
            
    #print "存在空气?", exist_air
    #print "存在水蒸气?", exist_steam
    #print "存在其他气体?", exist_other_g
        
        if items_calc[i].m_is_iu:  # step 1.2 : if not lbs or degree F, tranform unit into lbs or degree F
            items_calc[i].m = items_calc[i].m * HR_TO_SEC /COEF_1_LBS_TO_KG
        if items_calc[i].t_is_iu:
            t_degree_F = items_calc[i].t * (9.0 / 5) + 32
            items_calc[i].t = t_degree_F
            
    for i in items_calc:
    
        if (items_calc[i].name != "steam"):
        
            m_sum += items_calc[i].m
            try:
                n[i] = (items_calc[i].m / mole_weight[i])
                n_sum += n[i]
                print n[i]
            except (ZeroDivisionError):
                tkMessageBox.showerror("Data ERROR for mole weight","ZERO moleweight(moleweight = 0) for: " + items_calc[i].name)
                error_flag = True
            except:
                tkMessageBox.showerror("Data ERROR for mole weight","NO moleweight for: " + items_calc[i].name)
                error_flag = True
                
        temperature = items_calc[i].t
            
            
    ########## start calculation ##########
    if not error_flag:              # if data preprocessing succeed, then continue
    
        if exist_steam:             # if steam exists, then calculate it
            
            temp_m = items_calc["steam"].m / t_entrainment_ratio_STEAM(items_calc["steam"].t) # calculate equivalent_steam
            equivalent_steam = temp_m / 0.81
            
        if exist_air:             # if air exists, then calculate it
            
            equivalent_air = items_calc["air"].m / t_entrainment_ratio_AIR(items_calc["air"].t)# calculate equivalent_air
            
        if exist_other_g:
            print "m_sum = " + str(m_sum) + ", n_sum = " + str(n_sum)
            avg_moleweight = float(m_sum) / n_sum # calculate equivalent_mix_without_steam
            print avg_moleweight
            temp_m = m_sum / molewt_entrainment_ratio(avg_moleweight)
            print temp_m
            equivalent_mix_without_steam = temp_m / t_entrainment_ratio_AIR(temperature)
            print t_entrainment_ratio_AIR(temperature)
            print equivalent_mix_without_steam
        
            if exist_steam:
                
                equivalent_all = equivalent_steam + equivalent_mix_without_steam # equivalent_all = equivalent_steam + equivalent_mix_without_steam
                
            else:
            
                equivalent_all = equivalent_mix_without_steam # equivalent_all = equivalent_mix_without_steam
            
        elif (exist_air and exist_steam):
        
            equivalent_all = equivalent_steam + equivalent_air # equivalent_all = equivalent_steam + equivalent_air
            
        elif exist_steam:
        
            equivalent_all = equivalent_steam # equivalent_all = equivalent_steam
            
        else:
        
            equivalent_all = equivalent_air # equivalent_all = equivalent_air
        
        
        equivalent_all_iu = equivalent_all / (COEF_1_LBS_TO_KG * HR_TO_SEC)

        tkMessageBox.showinfo("Succeed!", "The result is: " + str(equivalent_all) + " lbs/hr or " + str(equivalent_all_iu) + "kg/s")
        
    else:
    
        tkMessageBox.showerror("Failed", "Please add enough data for moleweight, then try again.")
    
def t_entrainment_ratio_AIR(t): # Figure 15 (AIR)

    return (-0.0002403) * t + 1.018
    
def t_entrainment_ratio_STEAM(t): #Figure 15 (STEAM)

    return (-0.0003283) * t + 1.025
    
def molewt_entrainment_ratio(molewt):

    p1 = 0.0002718
    p2 = 1.78
    p3 = -89.8
    p4 = 1421
    p5 = -1416
    p6 = -234.4
    q1 = -28.48
    q2 = -292.6
    q3 = 1.646e+04
    q4 = -1.996e+04

    return (p1 * (molewt ** 5) + p2* (molewt ** 4) + p3* (molewt ** 3) + p4* (molewt ** 2) + p5 * molewt + p6) / (molewt ** 4 + q1 * molewt ** 3 + q2 * (molewt ** 2) + q3 * molewt + q4)
    
    
root = Tk()

app = App(root)

root.mainloop()
