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
names_chs = []

keyboard_option = {'m':False, 't':False}
text_variable = {'m':'', 't':''}

#以下字典保存计算结果。之所以采用全局变量，是为了减少计算量，即计算过的结果可保存在全局的字典中，如果下次计算时发现某温度组未发生变化，即可直接提取之前的计算结果
result_calc = {}
equivalent_all = {}
equivalent_all_SI = {}
equivalent_air = {}
equivalent_steam = {}
equivalent_mix_without_steam = {}

class Gas_item:

    def __init__(self, g_name, g_mass, g_unit_m, g_temperature, g_unit_t):

        self.name = g_name
        self.m = g_mass
        self.m_is_SI = g_unit_m
        self.t = g_temperature
        self.t_is_Celsius = g_unit_t

    def __str__(self):

        string_0 = "Gas name: " + name + "\n"

        if self.m_is_SI:
            mass_unit = " kg/s"
        else:
            mass_unit = " lbs/hr"
        string_1 = "Mass: " + str(m) + mass_unit + "\n"
  
        if self.t_is_Celsius:
            temp_unit = " degree C"
        else:
            temp_unit = " degree F"
        string_2 = "Temperature: " + str(t) + temp_unit + "\n"

        return string_0 + string_1 + string_2

class Keyboard():

    def __init__(self, masterbox, boxchoice):
    
        btn_calc = {}
        
        masterbox.protocol("WM_DELETE_WINDOW", self.quit_keyboard)#ref: http://115.28.181.12/questions/d7238b1fde95bb10cd70a558544d383ef1e0ccbb66503f89baab7c17335adf5f/
        keyboard_option[boxchoice] = True
        
        loc_i = 1
        
        self.framebox = masterbox
        self.txt_content = StringVar()
        self.keyboard_txt = Entry(masterbox, textvariable = self.txt_content)
        self.keyboard_txt.grid(row = 0, sticky = W) 
        self.whichbox = boxchoice
        
        btn_calc['1'] = Button(masterbox, text = '1', command = lambda: self.add_fig(1))
        btn_calc['2'] = Button(masterbox, text = '2', command = lambda: self.add_fig(2))
        btn_calc['3'] = Button(masterbox, text = '3', command = lambda: self.add_fig(3))
        btn_calc['4'] = Button(masterbox, text = '4', command = lambda: self.add_fig(4))
        btn_calc['5'] = Button(masterbox, text = '5', command = lambda: self.add_fig(5))
        btn_calc['6'] = Button(masterbox, text = '6', command = lambda: self.add_fig(6))
        btn_calc['7'] = Button(masterbox, text = '7', command = lambda: self.add_fig(7))
        btn_calc['8'] = Button(masterbox, text = '8', command = lambda: self.add_fig(8))
        btn_calc['9'] = Button(masterbox, text = '9', command = lambda: self.add_fig(9))
        btn_calc['0'] = Button(masterbox, text = "0", command = lambda: self.add_fig(0))
        
        btn_calc['POINT'] = Button(masterbox, text = ".", command = lambda: self.add_fig('.'))
        btn_calc['CLEAR'] = Button(masterbox, text = "C", command = self.clear_txt)

        for index in range(1, 10):
        
            if index % 3 == 1:
                delta_j = 0
            delta_j += 1
            btn_calc[str(index)].grid(row = int(math.ceil(float(index)/3)), column = loc_i + delta_j)
        
        btn_calc['0'].grid(row = 4, column = loc_i + 1)
        
        btn_calc['POINT'].grid(row = 4, column = loc_i + 2)
        btn_calc['CLEAR'].grid(row = 4, column = loc_i + 3)
        
        tempcontent = "将输入复制到主窗口"
        Button(masterbox, text = tempcontent.decode("GBK"), command = self.give_text).grid(row = 5)
        
        
    def add_fig(self, num):
        
        tempt = self.keyboard_txt.get()
        tempt += str(num)
        self.txt_content.set(tempt)
        
    def clear_txt(self):
        
        self.txt_content.set('')
        
    def give_text(self):
    
        text_variable[self.whichbox].set(self.keyboard_txt.get())
        keyboard_option[self.whichbox] = False
        self.quit_keyboard()
        
    def quit_keyboard(self):
    
        keyboard_option[self.whichbox] = False
        self.framebox.destroy()
        
def enter_mass():

    if not keyboard_option['m']:
        testbox1 = Toplevel()
        tempetitle = "质量："
        testbox1.title(tempetitle.decode("GBK"))
        mass_keyboard = Keyboard(testbox1, 'm')
    
def enter_temperature():

    if not keyboard_option['t']:
        testbox2 = Toplevel()
        tempetitle = "温度："
        testbox2.title(tempetitle.decode("GBK"))
        temperature_keyboard = Keyboard(testbox2, 't')
        
def read_data():
    
        global frame, read_success, frame, master, entry_mass, entry_temperature, item_option_var, unit_m, unit_t
        
        try:
            readf = open('MoleWT_data.txt', 'r')

            sum_items = int(readf.readline())

            for index in range(0, sum_items):
                temp_readl = readf.readline()
                j = 0
                key_chs = ''
                key_name = ''
                key_value = ''
                while (temp_readl[j] != ' '):
                    key_chs += temp_readl[j]
                    j += 1
                j += 1
                while (temp_readl[j] != ' '):
                    key_name += temp_readl[j]
                    j += 1
                j += 1
                while (temp_readl[j] != '\n'):
                    key_value += temp_readl[j]
                    j += 1
                mole_weight[key_name] = float(key_value)
                if not (0 < mole_weight[key_name] <= 150):
                    error_name_chs = key_chs.decode("GBK")
                    raise ZeroDivisionError
                names_options.append(key_name)
                names_chs.append(key_chs.decode("GBK"))


            readf.close()
            
            
            tempcontent = "添加/修改/删除"
            add_items_btn = Button(master, text=tempcontent.decode("GBK"), command=add_items) 
            add_items_btn.grid(row = 0, column = 4, sticky = E)
            
            tempcontent = "名称："
            label_name = Label(master, text = tempcontent.decode("GBK"))
            label_name.grid(row = 0, column = 2, sticky = W)
            
            item_option_var = StringVar(master)
            item_option_var.set(names_chs[0])
            item_option_menu = apply(OptionMenu, (master, item_option_var) + tuple(names_chs))             # http://effbot.org/tkinterbook/optionmenu.htm
            item_option_menu.grid(row = 0, column = 3, sticky = W)

            tempcontent = "质量："
            Button(master, text = tempcontent.decode("GBK"), command = enter_mass).grid(row = 2, column = 2, sticky = W)


            unit_m = IntVar() # True means kg, while False means lbs  # No need to be global variable
            unit_m.set(0)     # have to use variable class like IntVar(). simple int can't make the radiobutton know the group
            btn_unit_m_lbs = Radiobutton(master, text = "lbs/hr", variable = unit_m, value = 0)
            btn_unit_m_lbs.grid(row = 2, column = 3, sticky = W)
            btn_unit_m_kg = Radiobutton(master, text = "kg/s", variable = unit_m, value = 1)
            btn_unit_m_kg.grid(row = 3, column = 3, sticky = W)

            tempcontent = "温度：" # 文档应注明，0 ~ 1000 °F 或 0 ~ 537.778 °C
            Button(master, text = tempcontent.decode("GBK"), command = enter_temperature).grid(row = 4, column = 2, sticky = W)
            
            unit_t = IntVar() # True means degree C, while False means degree F # No need to be global variable
            unit_t.set(0)     # have to use variable class like IntVar(). simple int can't make the radiobutton know the group
            tempcontent = "°F"
            btn_unit_t_F = Radiobutton(master, text = tempcontent.decode("GBK"), variable = unit_t , value = 0)
            btn_unit_t_F.grid(row = 4, column = 3, sticky = W)
            tempcontent = "°C"
            btn_unit_t_C = Radiobutton(master, text = tempcontent.decode("GBK"), variable = unit_t, value = 1)
            btn_unit_t_C.grid(row = 5, column = 3, sticky = W)

            text_variable['m'] = StringVar()
            entry_mass = Entry(master, textvariable = text_variable['m'])
            entry_mass.grid(row = 3, column = 2, sticky = W)
            
            text_variable['t'] = StringVar()
            entry_temperature = Entry(master, textvariable = text_variable['t'])
            entry_temperature.grid(row = 5, column = 2, sticky = W)
            
        except ZeroDivisionError:
        
            temptitle = "分子量错误："
            tempcontent = "允许计算的分子量数值范围：大于 0，不超过 150。请检查并至少修改数据库中该项目的分子量："
            content_now = tempcontent.decode("GBK") + error_name_chs
            tkMessageBox.showerror(temptitle.decode("GBK"), content_now)
            master.destroy()

        except:
            temptitle = "错误"
            tempcontent = "文件损坏或不存在。请阅读帮助文档，修改或创建数据库文件。"
            tkMessageBox.showerror(temptitle.decode("GBK"), tempcontent.decode("GBK"))
            master.destroy()
        
def add_items():
    
        global button_number, master, entry_mass, entry_temperature, item_option_var, unit_m, unit_t, button_see_items, button_clear_items, button_calculation, listbox_items # must global entry_mass, entry_temperature, item_option_var, unit_m, unit_t, button_see_items, button_clear_items, button_calculation, listbox_items
        
        destroy_button = False#destroy_button = True
        
        valid_input = False # if data are all valid input, then transf2object 
        
        try:
            transf2mass = float(entry_mass.get())
            if (transf2mass < 0):
                raise TypeError
            valid_input = True
        except:
            temptitle = "输入错误：质量"
            tempcontent = "[质量]：请输入**非负数**"
            tkMessageBox.showerror(temptitle.decode("GBK"), tempcontent.decode("GBK"))
            
        try:
            transf2temp = float(entry_temperature.get())
            #检验温度是否在程序可计算范围内：0 ~ 1000 °F，即 0 ~ 537.778 °C
            if (unit_t.get() == 0):
                if (transf2temp < 70) or (transf2temp > 1000):
                    raise TypeError
            else:
                if (transf2temp < 21.111) or (transf2temp > 537.778):
                    raise TypeError
        except:
            temptitle = "输入错误：温度"
            tempcontent = "[温度]：请输入数字(70 ~ 1000 °F 或 21.111 ~ 537.778 °C)"
            tkMessageBox.showerror(temptitle.decode("GBK"), tempcontent.decode("GBK"))
            valid_input = False
            
       
        if valid_input:
        
            object_ei = Gas_item(names_options[names_chs.index(item_option_var.get())].lower(), transf2mass, unit_m.get(), transf2temp, unit_t.get())
        
            ##320150608继续改，最后一次改###############
            temperatureINDEX = float(str("%.2f" % transf2temp))
            
            if unit_t.get() == 1:
                temperatureINDEX = (temperatureINDEX * 9.0 / 5.0) + 32
                temperatureINDEX = float(str("%.2f" % temperatureINDEX))
            
            if (object_ei.m != 0):                                      #质量非 0
                if not str(temperatureINDEX) in items_wait4calc.keys():
                    items_wait4calc[str(temperatureINDEX)] = []
                    items_wait4calc[str(temperatureINDEX)].append(True) #items_wait4calc[str(temperatureINDEX)][0] 表示 「本轮计算中该组是否被修改过」，「是」 == True。新建立列表，显然被修改过，故直接赋值 True
                    items_wait4calc[str(temperatureINDEX)].append({})   #items_wait4calc[str(temperatureINDEX)][1] 用于存储温度 temperature 计算组
                items_wait4calc[str(temperatureINDEX)][1][object_ei.name] = object_ei 
                items_wait4calc[str(temperatureINDEX)][0] = True        #添加了新项目，则该温度组更新状态为「本轮计算中该组被修改过」
            else:                                                       #质量为 0
                if str(temperatureINDEX) in items_wait4calc.keys():     #若质量为 0 且存在该温度计算组，准备删除
                    if object_ei.name in items_wait4calc[str(temperatureINDEX)][1].keys():  #若质量为 0 且存在该温度计算组，且该计算组中存在该项目，则可以删除。以下分情况讨论
                        if len(items_wait4calc[str(temperatureINDEX)][1]) == 1:  
                            items_wait4calc.pop(str(temperatureINDEX)) 
                            if (len(items_wait4calc) == 0):
                                destroy_button = True
                                button_number = 0
                        else:  
                            items_wait4calc[str(temperatureINDEX)][1].pop(object_ei.name) 
                            items_wait4calc[str(temperatureINDEX)][0] = True        #删除项目，则该温度组更新状态为「本轮计算中该组被修改过」

            if (len(items_wait4calc) != 0):
                if (button_number == 0):
                    
                    button_number = 1
                    tempcontent = "已输入"
                    button_see_items = Button(master, text= tempcontent.decode("GBK"), command=see_items)
                    button_see_items.grid(row = 2, column = 4, sticky = E)
                    
                    tempcontent = "清空"
                    button_clear_items = Button(master, text= tempcontent.decode("GBK"), command=clear_items)
                    button_clear_items.grid(row = 6, column = 1, sticky = W + S)
                    tempcontent = "计算"
                    button_calculation = Button(master, text = tempcontent.decode("GBK"), command = calculation)
                    button_calculation.grid(row = 4, column = 4, sticky = E)
            elif destroy_button:
                button_see_items.destroy()
                button_clear_items.destroy()
                button_calculation.destroy()

def clear_items():

        global items_wait4calc, button_number, button_see_items, button_clear_items, button_calculation

        temptitle = "确认？"
        temptitleucode = temptitle.decode("GBK")
        tempcontent = "真的要清空当前所有输入吗？"
        tempcontentucode = tempcontent.decode("GBK")
        if tkMessageBox.askyesno(temptitleucode, tempcontentucode):
            items_wait4calc = {}
            button_number = 0
            button_see_items.destroy()
            button_clear_items.destroy()
            button_calculation.destroy()

def see_items():
        
        global items_wait4calc, name_chs
        
        content_now = ""
        
        for i in items_wait4calc:
        
            if items_wait4calc[i][0]:
            
                tempcontent = "*****上次计算后，以下部分刚修改过*****"
                content_now += tempcontent.decode("GBK")
                content_now += '\n'
        
            tempcontent = "温度："
            
            content_now += tempcontent.decode("GBK")
        
            content_now += ("%.2f " % float(i))
            
            tempcontent = "°F"
            content_now += tempcontent.decode("GBK")
            
            
            content_now += (' / %.2f ' % ((float(i) - 32)* 5.0 / 9.0))
            
            tempcontent = "°C"
            content_now += tempcontent.decode("GBK")
            
            content_now += '\n'
            
            for j in items_wait4calc[i][1]:
        
                tempcontent = "名称："
                content_now += tempcontent.decode("GBK")
                content_now += (names_chs[names_options.index(items_wait4calc[i][1][j].name)] + '  ')
                tempcontent = "质量："
                content_now += tempcontent.decode("GBK")
                content_now += str(items_wait4calc[i][1][j].m)
                
                if items_wait4calc[i][1][j].m_is_SI:
                    content_now += ' kg/s '
                else:
                    content_now += ' lbs/h '
                    
                tempcontent = "温度："
                content_now +=tempcontent.decode("GBK")
                content_now += ("%.2f \n" % items_wait4calc[i][1][j].t)
                
                if items_wait4calc[i][1][j].t_is_Celsius:
                    tempcontent = "°C"
                    content_now += tempcontent.decode("GBK")
                else:
                    tempcontent = "°F"
                    content_now += tempcontent.decode("GBK")
                    
                content_now += '\n'
                
            if items_wait4calc[i][0]:
            
                tempcontent = "*****上次计算后，以上部分刚修改过*****"
                content_now += tempcontent.decode("GBK")
                content_now += '\n'
            
            content_now += '\n'
            
        temptitle = "包含："
        temptitleucode = temptitle.decode("GBK")
        tkMessageBox.showinfo(temptitleucode, content_now)

def calculation():

    global items_wait4calc
    
    items_calc = items_wait4calc.copy()

    
    tempcontent = "温度为 "
    content_now = tempcontent.decode("GBK")
    
    icount = 1
    
    for i in items_calc:
    
        error_flag = False
        m_sum = 0
        n_sum = 0
        n = {}
        
        exist_air = False
        exist_steam = False
        exist_other_g = False
    
        if items_calc[i][0]:
        
            temperature = float(i)
            
            ########## step 1: data preprocessing ##########
            
            for j in items_calc[i][1]:
            
                if ("steam" == items_calc[i][1][j].name):            # step 1.1 : judge if air/steam/other gas
                    exist_steam = True
                elif ("air" == items_calc[i][1][j].name):
                    exist_air = True
                else:
                    exist_other_g = True
                
                if items_calc[i][1][j].m_is_SI:  # step 1.2 : if not lbs or degree F, tranform unit into lbs or degree F
                    items_calc[i][1][j].m = items_calc[i][1][j].m * HR_TO_SEC /COEF_1_LBS_TO_KG
                if items_calc[i][1][j].t_is_Celsius:
                    items_calc[i][1][j].t = float(i)
                    
            for j in items_calc[i][1]:
            
                if (items_calc[i][1][j].name != "steam"):
                
                    m_sum += items_calc[i][1][j].m

                    if (mole_weight[j] <= 0 or  mole_weight[j] > 150):
                        raise TypeError
                    n[j] = (items_calc[i][1][j].m / mole_weight[j])
                    n_sum += n[j]
                    
            ########## start calculation ##########
            if not error_flag:              # if data preprocessing succeed, then continue
            
                if exist_steam:             # if steam exists, then calculate it
                    
                    temp_m = items_calc[i][1]["steam"].m / t_entrainment_ratio_STEAM(items_calc[i][1]["steam"].t) # calculate equivalent_steam
                    equivalent_steam[i] = temp_m / 0.81
                    
                if exist_air:             # if air exists, then calculate it
                    
                    equivalent_air[i] = items_calc[i][1]["air"].m / t_entrainment_ratio_AIR(items_calc[i][1]["air"].t)# calculate equivalent_air
                    
                if exist_other_g:
                    avg_moleweight = float(m_sum) / n_sum # calculate equivalent_mix_without_steam
                    temp_m = m_sum / molewt_entrainment_ratio(avg_moleweight)
                    equivalent_mix_without_steam[i] = temp_m / t_entrainment_ratio_AIR(temperature)
                
                    if exist_steam:
                        
                        equivalent_all[i] = equivalent_steam[i] + equivalent_mix_without_steam[i] # equivalent_all = equivalent_steam + equivalent_mix_without_steam
                        
                    else:
                    
                        equivalent_all[i] = equivalent_mix_without_steam[i] # equivalent_all = equivalent_mix_without_steam
                    
                elif (exist_air and exist_steam):
                
                    equivalent_all[i] = equivalent_steam[i] + equivalent_air[i] # equivalent_all = equivalent_steam + equivalent_air
                    
                elif exist_steam:
                
                    equivalent_all[i] = equivalent_steam[i] # equivalent_all = equivalent_steam
                    
                else:
                
                    equivalent_all[i] = equivalent_air[i] # equivalent_all = equivalent_air
                
                
                equivalent_all_SI[i] = equivalent_all[i] / (COEF_1_LBS_TO_KG * HR_TO_SEC)
                
                result_calc[i] = []
                result_calc[i].append(equivalent_all[i])
                result_calc[i].append(equivalent_all_SI[i])

            else:
                temptitle = "失败："
                content_now = "请向数据库文件中添加足够的符合要求的分子量数据，然后再次尝试计算"
                tkMessageBox.showerror(temptitle.decode("GBK"), content_now.decode("GBK"))
                break
        
        if not error_flag:
            content_now += ("%.2f " % float(i))
            tempcontent = "°F"
            content_now += tempcontent.decode("GBK")
            content_now += (" / %.2f " % ((float(i) - 32) * 5.0 / 9.0))
            tempcontent = "°C"
            content_now += tempcontent.decode("GBK")
            content_now += ": \n"
            if items_calc[i][0]:
                tempcontent = "*****(新的计算组)*****"
                content_now += tempcontent.decode("GBK")
                content_now += '\n'
            content_now += "%.2f lbs/hr " % (equivalent_all[i])
            tempcontent = "或者"
            content_now += tempcontent.decode("GBK")
            content_now += " %.2f kg/s" % (equivalent_all_SI[i])
            
            icount += 1
            if icount <= len(items_calc):
                content_now += "\n\n"
                tempcontent = "温度为 "
                content_now += tempcontent.decode("GBK")
            

            
    if not error_flag:
        temptitle = "结果是："
        tkMessageBox.showinfo(temptitle.decode("GBK"), content_now)
        
    for i in items_calc:
    
        items_wait4calc[i][0] = False
            
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
temptitle = "空气当量换算"
master.title(temptitle.decode("GBK"))

read_data()

mainloop()
