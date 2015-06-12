# -*- coding: utf-8 -*-  
from Tkinter import *
import tkMessageBox
import math

COEF_1_LBS_TO_KG = 0.45359237 # 1 lbs = 0.45359237 kg
HR_TO_SEC = 3600 # 1 hr = 3600 s

items_wait4calc = {} # use dicts to add functions to the add button

read_success = False
button_number = 0

# 以下字典后期将与数据库连接，通过数据库进行存储、读取、修改等操作
mole_weight = {}  

names_options = []

class Gas_item:

    def __init__(self, g_name, g_mass, g_unit_m, g_temperature, g_unit_t):

        self.name = g_name
        self.m = g_mass
        self.m_is_iu = g_unit_m
        self.t = g_temperature
        self.t_is_iu = g_unit_t

    def __str__(self):

        string_0 = "Gas name: " + name + "\n"

        if self.m_is_iu:
            mass_unit = " kg/s"
        else:
            mass_unit = " lbs/hr"
        string_1 = "Mass: " + str(m) + mass_unit + "\n"
  
        if self.t_is_iu:
            temp_unit = " degree C"
        else:
            temp_unit = " degree F"
        string_2 = "Temperature: " + str(t) + temp_unit + "\n"

        return string_0 + string_1 + string_2



        
def read_data():
    
        global read_success, frame, master, entry_mass, entry_temperature, item_option_var, unit_m, unit_t
        
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

            names_options = list(mole_weight.keys())

            readf.close()
            tkMessageBox.showinfo(u'\u6210\u529f\uff01', u'\u8bfb\u5165\u6570\u636e\u5b8c\u6210\uff01') #tkMessageBox.showinfo("Succeed!", "Reading finished!")
            read_data_btn.destroy()
            frame.destroy()
            
            add_items_btn = Button(master, text=u'\u6dfb\u52a0/\u4fee\u6539/\u5220\u9664', command=add_items) #add_items_btn = Button(frame, text="Add/Modify/Delete", command=add_items)
            # using IDLE, input "添加/修改/删除".decode("GBK"), get u'\u6dfb\u52a0/\u4fee\u6539/\u5220\u9664', then copy this string {u'\u6dfb\u52a0/\u4fee\u6539/\u5220\u9664'}(withou {}) and paste here. see http://www.crifan.com/python_already_got_correct_encoding_string_but_seems_print_messy_code/
            add_items_btn.grid(row = 0, column = 4, sticky = E)
            
            # Panel 1 for Name
            label_name = Label(master, text = u'\u540d\u79f0\uff1a')#label_name = Label(m1, text = "Name: ")
            label_name.grid(row = 0, column = 2, sticky = W)
            
            item_option_var = StringVar(master)
            item_option_menu = apply(OptionMenu, (master, item_option_var) + tuple(names_options))             # http://effbot.org/tkinterbook/optionmenu.htm
            #entry_name = Entry(m1)
            item_option_menu.grid(row = 0, column = 3, sticky = W)

            label_mass = Label(master, text = u'\u8d28\u91cf\uff1a')#label_mass = Label(m2_1, text = "Mass: ")
            label_mass.grid(row = 2, column = 2, sticky = W)

            entry_mass = Entry(master)
            entry_mass.grid(row = 3, column = 2, sticky = W)

            unit_m = IntVar() # True means kg, while False means lbs  # No need to be global variable
            unit_m.set(0)     # have to use variable class like IntVar(). simple int can't make the radiobutton know the group
            btn_unit_m_lbs = Radiobutton(master, text = "lbs/hr", variable = unit_m, value = 0)
            btn_unit_m_lbs.grid(row = 2, column = 3, sticky = W)
            btn_unit_m_kg = Radiobutton(master, text = "kg/s", variable = unit_m, value = 1)
            btn_unit_m_kg.grid(row = 3, column = 3, sticky = W)

            label_temperature = Label(master, text = u'\u6e29\u5ea6\uff1a')#label_temperature = Label(m3_1, text = "Temperature: ")
            label_temperature.grid(row = 4, column = 2, sticky = W)

            entry_temperature = Entry(master)
            entry_temperature.grid(row = 5, column = 2, sticky = W)

            unit_t = IntVar() # True means degree C, while False means degree F # No need to be global variable
            unit_t.set(0)     # have to use variable class like IntVar(). simple int can't make the radiobutton know the group
            btn_unit_t_F = Radiobutton(master, text = u'\xb0F', variable = unit_t , value = 0)#btn_unit_t_F = Radiobutton(m3_2, text = "degree F", variable = unit_t , value = 0)
            btn_unit_t_F.grid(row = 4, column = 3, sticky = W)
            btn_unit_t_C = Radiobutton(master, text = u'\xb0C', variable = unit_t, value = 1)#btn_unit_t_C = Radiobutton(m3_2, text = "degree C", variable = unit_t, value = 1)
            btn_unit_t_C.grid(row = 5, column = 3, sticky = W)
        except:
            tkMessageBox.showerror(u'\u9519\u8bef', u'\u6587\u4ef6\u635f\u574f\u6216\u4e0d\u5b58\u5728\u3002\u8bf7\u9605\u8bfb\u5e2e\u52a9\u6587\u6863\uff0c\u4fee\u6539\u6216\u521b\u5efa\u6570\u636e\u5e93\u6587\u4ef6\u3002')#tkMessageBox.showerror("ERROR", "File BROKEN or NOT EXISTENT. Read documents, then modify or create the data file.")
        
def add_items():
    
        global button_number, master, entry_mass, entry_temperature, item_option_var, unit_m, unit_t, button_see_items, button_clear_items, button_calculation # must global entry_mass, entry_temperature, item_option_var, unit_m, unit_t, button_see_items, button_clear_items, button_calculation
        
        not_destroy_button = False
        
        valid_input = False # if data are all valid input, then transf2object 
        
        try:
            transf2mass = float(entry_mass.get())
            if (transf2mass < 0):
                raise TypeError
            valid_input = True
        except:
            tkMessageBox.showerror(u'\u8f93\u5165\u9519\u8bef\uff1a\u8d28\u91cf', u'[\u8d28\u91cf]\uff1a\u8bf7\u8f93\u5165**\u975e\u8d1f\u6570**')#tkMessageBox.showerror("Type ERROR for MASS", "Input NON-NEGATIVE-NUMBER for MASS please")
            
        try:
            transf2temp = float(entry_temperature.get())
        except:
            tkMessageBox.showerror(u'\u8f93\u5165\u9519\u8bef\uff1a\u6e29\u5ea6', u'[\u6e29\u5ea6]\uff1a\u8bf7\u8f93\u5165\u6570\u5b57')#tkMessageBox.showerror("Type ERROR for TEMPERATURE", "Input NUMBER for TEMPERATURE please")
            valid_input = False
            
        if valid_input:
            object_ei = Gas_item(item_option_var.get().lower(), transf2mass, unit_m.get(), transf2temp, unit_t.get())
        
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
                    button_see_items = Button(master, text=u'\u5df2\u8f93\u5165', command=see_items)#button_see_items = Button(frame, text="Already", command=see_items)
                    button_see_items.grid(row = 2, column = 4, sticky = E)
                    button_clear_items = Button(master, text=u'\u6e05\u7a7a', command=clear_items)#button_clear_items = Button(frame, text="Clear", command=clear_items)
                    button_clear_items.grid(row = 6, column = 1, sticky = W + S)
                    button_calculation = Button(master, text = u'\u8ba1\u7b97', command = calculation)#button_calculation = Button(frame, text = "CALC", command = calculation)
                    button_calculation.grid(row = 4, column = 4, sticky = E)
            elif not not_destroy_button:
                button_see_items.destroy()               # must add 0 judgement here
                button_clear_items.destroy()
                button_calculation.destroy()

def clear_items():

        global items_wait4calc, button_number, button_see_items, button_clear_items, button_calculation

        temptitle = "确认？"
        temptitleucode = temptitle.decode("GBK")
        tempcontent = "真的要清空当前所有输入吗？"
        tempcontentucode = tempcontent.decode("GBK")  # experiment succeed. we don't need to use IDLE to transform code
        if tkMessageBox.askyesno(temptitleucode, tempcontentucode):
            items_wait4calc = {}
            button_number = 0
            button_see_items.destroy()
            button_clear_items.destroy()
            button_calculation.destroy()

            
def see_items():
        
        global items_wait4calc
        
        content_now = ""
        
        for i in items_wait4calc:
        
            content_now += (u'\u540d\u79f0\uff1a' + items_wait4calc[i].name + u'\u8d28\u91cf\uff1a' + str(items_wait4calc[i].m))#content_now += ('Name: ' + items_wait4calc[i].name + ' Mass:' + str(items_wait4calc[i].m))
            
            if items_wait4calc[i].m_is_iu:
                content_now += ' kg/s'
            else:
                content_now += ' lbs/h'
                
            content_now += (' ' + u'\u6e29\u5ea6\uff1a' + str(items_wait4calc[i].t) + '\n')#content_now += (' Temperature:' + str(items_wait4calc[i].t) + '\n')
            
            if items_wait4calc[i].t_is_iu:
                content_now += (' ' + u'\xb0C')
            else:
                content_now += (' ' + u'\xb0F')
                
            content_now += '\n'
            
        tkMessageBox.showinfo(u'\u5305\u542b\uff1a', content_now)
        
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
            except (ZeroDivisionError):
                tkMessageBox.showerror(u'\u6570\u636e\u9519\u8bef\uff1a\u5206\u5b50\u91cf',u'\u5bf9\u4e8e\u8be5\u9879\u76ee\uff0c\u60a8\u63d0\u4f9b\u7684\u5206\u5b50\u91cf\u4e3a 0\uff0c\u8fd9\u662f\u9519\u8bef\u7684\uff0c\u8bf7\u66f4\u6539\uff1a' + items_calc[i].name)#tkMessageBox.showerror("Data ERROR for mole weight","ZERO moleweight(moleweight = 0) for: " + items_calc[i].name)
                error_flag = True
            #except:
                #tkMessageBox.showerror(u'\u6570\u636e\u9519\u8bef\uff1a\u5206\u5b50\u91cf',u'\u7f3a\u5c11\u8be5\u9879\u76ee\u7684\u5206\u5b50\u91cf\uff1a' + items_calc[i].name)#tkMessageBox.showerror("Data ERROR for mole weight","NO moleweight for: " + items_calc[i].name)
                #error_flag = True
                
        temperature = items_calc[i].t
            
            
    ########## start calculation ##########
    if not error_flag:              # if data preprocessing succeed, then continue
    
        if exist_steam:             # if steam exists, then calculate it
            
            temp_m = items_calc["steam"].m / t_entrainment_ratio_STEAM(items_calc["steam"].t) # calculate equivalent_steam
            equivalent_steam = temp_m / 0.81
            
        if exist_air:             # if air exists, then calculate it
            
            equivalent_air = items_calc["air"].m / t_entrainment_ratio_AIR(items_calc["air"].t)# calculate equivalent_air
            
        if exist_other_g:
            avg_moleweight = float(m_sum) / n_sum # calculate equivalent_mix_without_steam
            temp_m = m_sum / molewt_entrainment_ratio(avg_moleweight)
            equivalent_mix_without_steam = temp_m / t_entrainment_ratio_AIR(temperature)
        
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

        tkMessageBox.showinfo(u'\u6210\u529f\uff01', u'\u7ed3\u679c\u662f\uff1a' + str(equivalent_all) + " lbs/hr " + u'\u6216\u8005 ' + str(equivalent_all_iu) + "kg/s")#tkMessageBox.showinfo("Succeed!", "The result is: " + str(equivalent_all) + " lbs/hr or " + str(equivalent_all_iu) + "kg/s")
        
    else:
    
        tkMessageBox.showerror(u'\u5931\u8d25\u4e86...', u'\u8bf7\u5411\u6570\u636e\u5e93\u6587\u4ef6\u4e2d\u6dfb\u52a0\u8db3\u591f\u7684\u5206\u5b50\u91cf\u6570\u636e\uff0c\u7136\u540e\u518d\u6b21\u5c1d\u8bd5\u8ba1\u7b97')#tkMessageBox.showerror("Failed", "Please add enough data for moleweight, then try again.")
    
def t_entrainment_ratio_AIR(t): # Figure 15 (AIR)

    return (-0.0002403) * t + 1.018
    
def t_entrainment_ratio_STEAM(t): # Figure 15 (STEAM)

    return (-0.0003283) * t + 1.025
    
def molewt_entrainment_ratio(molewt):  # Figure 16

    p1 =  1.855
    p2 = -69.42
    p3 =  739.4
    p4 =  56.39
    p5 = -1522
    p6 = -18.26
    q1 = -13.57
    q2 = -499.7
    q3 =  9868
    q4 = -5746
    q5 = -1.192e+04

    return (p1* (molewt ** 5) + p2* (molewt ** 4) + p3 * (molewt ** 3) + p4 * (molewt ** 2) + p5 * molewt + p6) / ((molewt ** 5) + q1 * (molewt ** 4) + q2 * (molewt ** 3) + q3 * (molewt ** 2) + q4 * molewt + q5)
    
    
master = Tk()

        
frame = Frame(master)
frame.pack()

read_data_btn = Button(master, text = u'\u8bfb\u53d6', command = read_data)#read_data_btn = Button(frame, text = "Read", command = read_data)
read_data_btn.pack(side = LEFT)

mainloop()
