# coding: utf-8
from Tkinter import *
import tkMessageBox

items_wait4calc = []
content_now = ""
exist_air = False
exist_steam = False
exist_other_g = False
equivalent_all = 0

# 以下字典后期将与数据库连接，通过数据库进行存储、读取、修改等操作
mole_weight = {
              "air":29,
              "steam":18,
              "hydrogen":2,
              "ammonia":17
              }
        
def t_vs_entrainment_ratio_air(t):
    return (-0.0002403) * t + 1.018 # 此处用 图15 温度-引射系数 空气 曲线方程代替 Replace with proper function        
    
def t_vs_entrainment_ratio_steam(t):
    return (-0.0003283) * t + 1.025 # 此处用 图15 温度-引射系数 水蒸气 曲线方程代替 Replace with proper function    
        
def mole_wt_vs_entrainment_ratio(wt):
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

    return (p1 * (molewt ** 5) + p2* (molewt ** 4) + p3* (molewt ** 3) + p4* (molewt ** 2) + p5 * molewt + p6) / (molewt ** 4 + q1 * molewt ** 3 + q2 * (molewt ** 2) + q3 * molewt + q4) # 此处用 图16 分子量-引射系数 曲线方程代替 Replace with proper function    

def steam_air_prop_vs_entrainment_ratio(p, temp_air):
    return int(p * 100) + temp_air * 1# 此处用 图17 水蒸气-空气百分比-引射系数 曲线方程代替 Replace with proper function            

              

class Gas_item:

    def __init__(self, g_name, g_mass, g_mass_is_iu, g_temperature, g_temp_is_iu):
    
        self.name = g_name
        self.m = g_mass
        self.m_is_iu = g_mass_is_iu
        self.t = g_temperature
        self.t_is_iu = g_temp_is_iu
        
    def __str__(self):
    
        string_0 = "Gas name: " + self.name + "\n"

        if (True == self.m_is_iu):
            mass_unit = " kg"
        else:
            mass_unit = " lbs"
        string_1 = "Mass: " + str(self.m) + mass_unit + "\n"
        
        if (True == self.t_is_iu):
            temp_unit = " degree C"
        else:
            temp_unit = " degree F"
        string_2 = "Temperature: " + str(self.t) + temp_unit + "\n"
        
        return string_0 + string_1 + string_2

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        # Button-design 按钮设计
        
        #self.button = Button(
        #    frame, text="QUIT", fg="red", command=frame.quit
        #    )
        #self.button.pack(side=LEFT)
        
        self.add_items_buton = Button(frame, text="添加项目", command=self.add_items)
        self.add_items_buton.pack(side=LEFT)
        
        self.see_items_buton = Button(frame, text="已添加项目", command=self.see_items)
        self.see_items_buton.pack(side=LEFT)
        
        self.clear_items_buton = Button(frame, text="清空", command=self.clear_items)
        self.clear_items_buton.pack(side=LEFT)

        self.start_calc_button = Button(frame, text="开始换算", command=self.calc)
        self.start_calc_button.pack(side=LEFT)
        
        # Text-entry 文本输入
        text_label = Label(master, text ="格式：名称#宏观质量#(Y/G)#宏观温度#(Y/G)\n注：(Y/G)处输入Y还是G的依据是前一项输入的单位制\n英制单位数值则输入Y，公制单位数值则输入G\n英制单位指 lbs °F\n公制单位指 kg °C\n目前仅支持**英文**输入")
        text_label.pack()
        self.e = Entry(master)
        self.e.pack()
        self.e.insert(0, "按格式输入")
        
    def calc(self):      # 未增加单位换算模块。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。
    
        global exist_air, exist_steam, exist_other_g, equivalent_all
        
        equivalent_steam = 0
        equivalent_air = 0
        equivalent_blend_air_steam = 0
        equivalent_other_g = 0
        equivalent_all = 0
        
        if exist_other_g:  # 目前视非空气且非水蒸气的其他气体在同一气体混合物中，即温度视为一致，此处或可尝试优化。。。。。。。。。。。。。。。。。。。
            sum_moles = 0  # 求其他气体的平均分子量
            sum_mass = 0
            for i in items_wait4calc:
                if (("steam" != i.name) and ("air" != i.name)):
                    sum_moles += i.m / mole_weight[i.name]
                    sum_mass += i.m
                    temp_other_g = i.t
            avg_mole_wt = sum_mass / sum_moles
            equivalent_other_g_after_mole_wt = sum_mass / mole_wt_vs_entrainment_ratio(avg_mole_wt)           # 图16
            equivalent_other_g = equivalent_other_g_after_mole_wt / t_vs_entrainment_ratio_air(temp_other_g)  # 图15，水蒸气、空气以外的气体混合物对应空气当量
        
        sum_mass_blend_air_steam = 0      # 目前若空气水蒸气同时存在，则视为在同一混合物中，温度视为一致，此处或可尝试优化。。。。。。。。。。。。。。。。。。。
        sum_mass_air = 0
        sum_mass_steam = 0
        for i in items_wait4calc:
            if ("air" == i.name):
                sum_mass_air += i.m
                temp_air = i.t
            if ("steam" == i.name):
                sum_mass_steam += i.m
                temp_steam = i.t
        sum_mass_blend_air_steam = sum_mass_air + sum_mass_steam
        if (exist_steam and exist_air):
            prop = sum_mass_air / sum_mass
            equivalent_blend_air_steam = steam_air_prop_vs_entrainment_ratio(prop, temp_air)   # 图17，当在温度为 temp_air 的总混合物中空气所占质量比例为 prop 时，空气-水蒸气混合物对应的空气当量
        elif exist_steam:                                                                      # 若只有水蒸气
            equivalent_steam_after_mole_wt = sum_mass_steam / 0.875  # 图16
            equivalent_steam = equivalent_steam_after_mole_wt / t_vs_entrainment_ratio_steam(temp_steam) # 图15
        else:                                                                                  # 若只有空气
            equivalent_air = sum_mass_air / t_vs_entrainment_ratio_air(temp_air)               # 图15
            
        equivalent_all = equivalent_other_g + equivalent_blend_air_steam + equivalent_steam + equivalent_air
        tkMessageBox.showinfo("总换算当量为...", str(equivalent_all) + "lbs/hr")
        
    def add_items(self):
        ei = self.e.get() # ei = element(i)
        object_ei = self.transf_ei_to_g_item(ei) # transform string ei to an instance of class Gas_item
        items_wait4calc.append(object_ei) # add this new object into the list
            
    def transf_ei_to_g_item(self, wait4transf):
        global exist_air, exist_other_g, exist_steam
        i = 0
        # 当输入不符合格式，例如到尾部一直都找不到 # 时，应给出错误提示。。。。。待增加
        
        # get the name of new input
        name = "" 
        while('#' != wait4transf[i]):
            name += wait4transf[i]
            i += 1
        if (name.isalpha()):
            name = name.lower()
        if ("air" == name):
            exist_air = True
        elif("steam" == name):
            exist_steam = True
        else:
            exist_other_g = True
        
        # get the mass of new input
        i += 1
        wait4transf2mass = ""
        while('#' != wait4transf[i]):
            wait4transf2mass += wait4transf[i]
            i += 1
        transf2mass = float(wait4transf2mass)  # ValueError......待增补处理方式
        
        # get the mass of new input
        i += 1
        jg_mass_iu = True
        if ("G" == wait4transf[i]):
            jg_mass_iu = True
        elif ("Y" == wait4transf[i]):
            jg_mass_iu = False
        #else:                       # 既不是公制也不是英制单位时，出错......待增补处理方式
        #    jg_mass_iu = True
        
        # get the temperature of new input
        i += 2  # 上次读取到 Y 或 G，下一个字符是 # 分隔符，再下一个才是温度
        wait4transf2temp = ""
        while('#' != wait4transf[i]):
            wait4transf2temp += wait4transf[i]
            i += 1
        transf2temp = float(wait4transf2temp)  # ValueError......待增补处理方式
        
        # get the mass of new input
        i += 1
        jg_temp_iu = True
        if ("G" == wait4transf[i]):
            jg_temp_iu = True
        elif ("Y" == wait4transf[i]):
            jg_temp_iu = False
        #else:                       # 既不是公制也不是英制单位时，出错......待增补处理方式
        #    jg_temp_iu = True
        
        transf2object = Gas_item(name, transf2mass, jg_mass_iu, transf2temp, jg_temp_iu)
        
        return transf2object # tran2item is an instance of class Gas_item
        
    def see_items(self):
        global content_now
        content_now = ""
        for i in items_wait4calc:
            content_now += ('Name: ' + i.name + ' Mass:' + str(i.m) + ' Temperature:' + str(i.t) + '\n')
        tkMessageBox.showinfo("已经添加了...", content_now)
        
    def clear_items(self):
        global items_wait4calc
        items_wait4calc = []
    
root = Tk()

app = App(root)

root.mainloop()
