import os
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import time 
import datetime
import matplotlib.dates as mdates
import rpyc
from quickle import dumps, loads
def plot_power_lv_status():  
    #conn = sqlite3.connect('test2.db')
    #cursor = conn.cursor()
    conn= rpyc.connect('127.0.0.1', 44555)

    #print lv of two even layer(0,2)
    plt.figure(figsize=(1200/100, 400/100), dpi=100)
    plt.xlim(0,12)
    plt.ylim(0,4)
    for i in range(0,3,2):
        for j in range(6):
            k=i/2
            crate = i % 2
            card = i + (i + 1) % 2 + j // 3 
            if j%3==0:
                connector='a'
                
            elif j%3==1:
                connector='b'
                
            else:
                connector='c'
                
            if i==1 and j==2:
                crate==1
                card=9
                connector='b'
                
            if i==5 and j==2:
                crate==1
                card=9
                connector='c'
            #get data
            sql=f"SELECT lv_d3v8_{connector}, lv_d2v8_{connector}, lv_a2v8_{connector}, lv_a3v3_{connector} ,lv_d3i8_{connector}, lv_d2i8_{connector}, lv_a2i8_{connector}, lv_a3i3_{connector} from tracker_power WHERE crate = {crate} AND card = {card}  order by gcutime desc limit 1;"
            data=conn.root.query(sql)
            LV = loads(data)
            #get status: on or off 
            color_IF = '#FFC0CB'if LV[-1][0]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_digital = '#FFC0CB'if LV[-1][1]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_analog = '#FFC0CB'if LV[-1][2]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_calibration = '#FFC0CB'if LV[-1][3]>=2000 and LV[-1][6]>100 else '#CAEBD8'
           
            #print status and value
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [0, 0, 1, 1], color=color_IF)
            plt.text(j+k*6+0.5, 0.75, f'{ LV[-1][0]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.5, 0.25, f'{LV[-1][4]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [1, 1,2,2], color=color_digital)
            plt.text(j+k*6+0.5, 1.75, f'{ LV[-1][1]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.5, 1.25, f'{LV[-1][5]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [2, 2, 3, 3], color=color_analog) 
            plt.text(j+k*6+0.5, 2.75, f'{ LV[-1][2]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.5, 2.25, f'{LV[-1][6]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [3, 3, 4, 4], color=color_calibration)
            plt.text(j+k*6+0.5, 3.75, f'{ LV[-1][3]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey') 
            plt.text(j+k*6+0.5, 3.25, f'{LV[-1][7]}mA', ha='center', va='center', fontsize=10,color='b')
            
    for i in range(5):
        ax.axhline(y=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(24):
        ax.axvline(x=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(1, 4):
        ax.axvline(x=i * 6, color='black', linestyle='-', linewidth=2)
    plt.grid(True, linestyle='--', linewidth=0.5)
    ax.set_xticks([i + 0.5 for i in range(12)], [f'ROW {i //6 *2}{i%6}' for i in range(12)])
    ax.tick_params(axis='x',length=0)
    ax.set_yticks([i * 1+ 0.5 for i in range(4)], ['IF','Digital','Analog','Calibration'])
    plt.tight_layout()
    plt.savefig('./static/images/power_status_lv_even_1.png') 
    plt.close()


    #print lv of two even layer(4,6)
    plt.figure(figsize=(1200/100, 400/100), dpi=100)
    plt.xlim(0,12)
    plt.ylim(0,4)
    for i in range(4,7,2):
        for j in range(6):
            k=(i-4)/2
            crate = i % 2
            card = i + (i + 1) % 2 + j // 3 
            if j%3==0:
                connector='a'
                
            elif j%3==1:
                connector='b'
                
            else:
                connector='c'
                
            if i==1 and j==2:
                crate==1
                card=9
                connector='b'
                
            if i==5 and j==2:
                crate==1
                card=9
                connector='c'
            #get data 
            sql=f"SELECT lv_d3v8_{connector}, lv_d2v8_{connector}, lv_a2v8_{connector}, lv_a3v3_{connector} ,lv_d3i8_{connector}, lv_d2i8_{connector}, lv_a2i8_{connector}, lv_a3i3_{connector} from tracker_power WHERE crate = {crate} AND card = {card}  order by gcutime desc limit 1;"
            data=conn.root.query(sql)
            LV = loads(data)
    
            color_IF = '#FFC0CB'if LV[-1][0]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_digital = '#FFC0CB'if LV[-1][1]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_analog = '#FFC0CB'if LV[-1][2]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_calibration = '#FFC0CB'if LV[-1][3]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [0, 0, 1, 1], color=color_IF)
            plt.text(j+k*6+0.5, 0.75, f'{ LV[-1][0]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.5, 0.25, f'{LV[-1][4]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [1, 1,2,2], color=color_digital)
            plt.text(j+k*6+0.5, 1.75, f'{ LV[-1][1]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.5, 1.25, f'{LV[-1][5]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [2, 2, 3, 3], color=color_analog) 
            plt.text(j+k*6+0.5, 2.75, f'{ LV[-1][2]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.5, 2.25, f'{LV[-1][6]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [3, 3, 4, 4], color=color_calibration)
            plt.text(j+k*6+0.5, 3.75, f'{ LV[-1][3]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey') 
            plt.text(j+k*6+0.5, 3.25, f'{LV[-1][7]}mA', ha='center', va='center', fontsize=10,color='b')
            
    for i in range(5):
        ax.axhline(y=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(24):
        ax.axvline(x=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(1, 4):
        ax.axvline(x=i * 6, color='black', linestyle='-', linewidth=2)
    plt.grid(True, linestyle='--', linewidth=0.5)
    ax.set_xticks([i +0.5 for i in range(12)], [f'ROW {i //6 *2+4}{i%6}' for i in range(12)])
    ax.set_yticks([i * 1+ 0.5 for i in range(4)], ['IF','Digital','Analog','Calibration'])
    plt.tight_layout()
    plt.savefig('./static/images/power_status_lv_even_2.png') 
    plt.close()


    #print lv of two odd layer(1,3,5)
    plt.figure(figsize=(1800/100, 400/100), dpi=100)
    plt.xlim(0,18)
    plt.ylim(0,4)
    for i in range(1,7,2):
        for j in range(6):
            k=(i-1)/2
            crate = i % 2
            card = i + (i + 1) % 2 + j // 3 
            if j%3==0:
                connector='a'  
            elif j%3==1:
                connector='b'
            else:
                connector='c'
            if i==1 and j==2:
                crate==1
                card=9
                connector='b'
            if i==5 and j==2:
                crate==1
                card=9
                connector='c'
            #get data
            sql=f"SELECT lv_d3v8_{connector}, lv_d2v8_{connector}, lv_a2v8_{connector}, lv_a3v3_{connector} ,lv_d3i8_{connector}, lv_d2i8_{connector}, lv_a2i8_{connector}, lv_a3i3_{connector} from tracker_power WHERE crate = {crate} AND card = {card}  order by gcutime desc limit 1;"
            data=conn.root.query(sql)
            LV = loads(data)
        
            color_IF = '#FFC0CB'if LV[-1][0]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_digital = '#FFC0CB'if LV[-1][1]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_analog = '#FFC0CB'if LV[-1][2]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_calibration = '#FFC0CB'if LV[-1][3]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [0, 0, 1, 1], color=color_IF)
            plt.text(j+k*6+0.5, 0.75, f'{ LV[-1][0]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.5, 0.25, f'{LV[-1][4]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [1, 1,2,2], color=color_digital)
            plt.text(j+k*6+0.5, 1.75, f'{ LV[-1][1]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.5, 1.25, f'{LV[-1][5]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [2, 2, 3, 3], color=color_analog) 
            plt.text(j+k*6+0.5, 2.75, f'{ LV[-1][2]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.5, 2.25, f'{LV[-1][6]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [3, 3, 4, 4], color=color_calibration)
            plt.text(j+k*6+0.5, 3.75, f'{ LV[-1][3]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey') 
            plt.text(j+k*6+0.5, 3.25, f'{LV[-1][7]}mA', ha='center', va='center', fontsize=10,color='b')
            
    for i in range(5):
        ax.axhline(y=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(18):
        ax.axvline(x=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(1, 3):
        ax.axvline(x=i * 6, color='black', linestyle='-', linewidth=2)
    plt.grid(True, linestyle='--', linewidth=0.5)
    ax.set_xticks([i +0.5 for i in range(18)], [f'ROW {i //6 *2+1}{i%6}' for i in range(18)])
    ax.set_yticks([i * 1+ 0.5 for i in range(4)], ['IF','Digital','Analog','Calibration'])
    plt.tight_layout()
    plt.savefig('./static/images/power_status_lv_odd.png') 
    plt.close()




def plot_power_hv_status():
    conn= rpyc.connect('127.0.0.1', 44555)
    plt.figure(figsize=(1200/100, 400/100), dpi=100)
    plt.xlim(0,12)
    plt.ylim(0,6)
    for i in range(0,3,2):
        for j in range(6):
            k=i/2
            crate = i % 2
            card = i + (i + 1) % 2 + j // 3
            if j%3==0:
                connector='a'
                channel=1
            elif j%3==1:
                connector='b'
                channel=7
            else:
                connector='c'
                channel=13
            if i==1 and j==2:
                crate==1
                card=9
                connector='b'
                channel=7
            if i==5 and j==2:
                crate==1
                card=9
                connector='c'
                channel=13
            
            sql=f"SELECT hv_voltage_{channel},hv_voltage_{channel+1},hv_voltage_{channel+2},hv_voltage_{channel+3},hv_voltage_{channel+4},hv_voltage_{channel+5},hv_current_{channel},hv_current_{channel+1},hv_current_{channel+2},hv_current_{channel+3},hv_current_{channel+4},hv_current_{channel+5} from tracker_power WHERE crate = {crate} AND card = {card}  order by gcutime desc limit 1;"
            data=conn.root.query(sql)
            HV = loads(data)

            color_m0='#FFC0CB' if HV[-1][0]>=200 and HV[-1][6]<=5900 and HV[-1][0]<=1000 else '#CAEBD8'
            color_m1='#FFC0CB'if HV[-1][1]>=200 and HV[-1][7]<=5900 and HV[-1][1]<=1000 else '#CAEBD8'
            color_m2='#FFC0CB'if HV[-1][2]>=200 and HV[-1][8]<=5900 and HV[-1][2]<=1000 else '#CAEBD8'
            color_m3='#FFC0CB'if HV[-1][3]>=200 and HV[-1][9]<=5900 and HV[-1][3]<=1000 else '#CAEBD8'
            color_m4='#FFC0CB'if HV[-1][4]>=200 and HV[-1][10]<=5900 and HV[-1][4]<=1000 else '#CAEBD8'
            color_m5='#FFC0CB'if HV[-1][5]>=200 and HV[-1][11]<=5900 and HV[-1][5]<=1000 else '#CAEBD8'
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [0, 0, 1, 1], color=color_m0)
            plt.text(j+k*6+0.25, 0.70, f'{HV[-1][0]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 0.25, f'{HV[-1][6]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[0,1],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [1, 1, 2, 2], color=color_m1)
            plt.text(j+k*6+0.25, 1.70, f'{HV[-1][1]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 1.25, f'{HV[-1][7]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[1,2],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [2, 2, 3, 3], color=color_m2)
            plt.text(j+k*6+0.25, 2.70, f'{HV[-1][2]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 2.25, f'{HV[-1][8]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[2,3],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [3, 3, 4, 4], color=color_m3)
            plt.text(j+k*6+0.25, 3.70, f'{HV[-1][3]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 3.25, f'{HV[-1][9]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[3,4],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [4, 4, 5, 5], color=color_m4)
            plt.text(j+k*6+0.25, 4.70, f'{HV[-1][4]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 4.25, f'{HV[-1][10]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[4,5],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [5, 5, 6, 6], color=color_m5)
            plt.text(j+k*6+0.25, 5.70, f'{HV[-1][5]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 5.25, f'{HV[-1][11]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[5,6],color='white',linestyle='dashed', linewidth=1)
    
    for i in range(12):
        ax.axvline(x=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(6):
        ax.axhline(y=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(1, 3):
        ax.axvline(x=i * 6, color='black', linestyle='-', linewidth=2)
    plt.grid(True, linestyle='--', linewidth=0.5)
    ax.set_xticks([i +0.5 for i in range(12)], [f'ROW {i //6 *2}{i%6}' for i in range(12)])
    ax.set_yticks([i+0.5  for i in range(6)], [f'Mod {i}' for i in range(6)])
    plt.tight_layout()
    plt.savefig('./static/images/power_status_hv_even_1.png')   
    plt.close()


    plt.figure(figsize=(1200/100, 400/100), dpi=100)
    plt.xlim(0,12)
    plt.ylim(0,6)
    for i in range(4,7,2):
        for j in range(6):
            k=(i-4)/2
            crate = i % 2
            card = i + (i + 1) % 2 + j // 3
            if j%3==0:
                connector='a'
                channel=1
            elif j%3==1:
                connector='b'
                channel=7
            else:
                connector='c'
                channel=13
            if i==1 and j==2:
                crate==1
                card=9
                connector='b'
                channel=7
            if i==5 and j==2:
                crate==1
                card=9
                connector='c'
                channel=13
            
            sql=f"SELECT hv_voltage_{channel},hv_voltage_{channel+1},hv_voltage_{channel+2},hv_voltage_{channel+3},hv_voltage_{channel+4},hv_voltage_{channel+5},hv_current_{channel},hv_current_{channel+1},hv_current_{channel+2},hv_current_{channel+3},hv_current_{channel+4},hv_current_{channel+5} from tracker_power WHERE crate = {crate} AND card = {card}  order by gcutime desc limit 1;"
            data=conn.root.query(sql)
            HV = loads(data)
            
            color_m0='#FFC0CB'if HV[-1][0]>=200 and HV[-1][6]<=5900 and HV[-1][0]<=1000 else '#CAEBD8'
            color_m1='#FFC0CB'if HV[-1][1]>=200 and HV[-1][7]<=5900 and HV[-1][1]<=1000 else '#CAEBD8'
            color_m2='#FFC0CB'if HV[-1][2]>=200 and HV[-1][8]<=5900 and HV[-1][2]<=1000 else '#CAEBD8'
            color_m3='#FFC0CB'if HV[-1][3]>=200 and HV[-1][9]<=5900 and HV[-1][3]<=1000 else '#CAEBD8'
            color_m4='#FFC0CB'if HV[-1][4]>=200 and HV[-1][10]<=5900 and HV[-1][4]<=1000 else '#CAEBD8'
            color_m5='#FFC0CB'if HV[-1][5]>=200 and HV[-1][11]<=5900 and HV[-1][5]<=1000 else '#CAEBD8'
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [0, 0, 1, 1], color=color_m0)
            plt.text(j+k*6+0.25, 0.70, f'{HV[-1][0]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 0.25, f'{HV[-1][6]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[0,1],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [1, 1, 2, 2], color=color_m1)
            plt.text(j+k*6+0.25, 1.70, f'{HV[-1][1]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 1.25, f'{HV[-1][7]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[1,2],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [2, 2, 3, 3], color=color_m2)
            plt.text(j+k*6+0.25, 2.70, f'{HV[-1][2]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 2.25, f'{HV[-1][8]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[2,3],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [3, 3, 4, 4], color=color_m3)
            plt.text(j+k*6+0.25, 3.70, f'{HV[-1][3]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 3.25, f'{HV[-1][9]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[3,4],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [4, 4, 5, 5], color=color_m4)
            plt.text(j+k*6+0.25, 4.70, f'{HV[-1][4]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 4.25, f'{HV[-1][10]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[4,5],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [5, 5, 6, 6], color=color_m5)
            plt.text(j+k*6+0.25, 5.70, f'{HV[-1][5]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 5.25, f'{HV[-1][11]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[5,6],color='white',linestyle='dashed', linewidth=1)
    
    for i in range(12):
        ax.axvline(x=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(6):
        ax.axhline(y=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(1, 3):
        ax.axvline(x=i * 6, color='black', linestyle='-', linewidth=2)
    plt.grid(True, linestyle='--', linewidth=0.5)
    ax.set_xticks([i +0.5 for i in range(12)], [f'ROW {i //6 *2+4}{i%6}' for i in range(12)])
    ax.set_yticks([i+1/2  for i in range(6)], [f'Mod {i}' for i in range(6)])
    plt.tight_layout()
    plt.savefig('./static/images/power_status_hv_even_2.png')   
    plt.close()


    
    plt.figure(figsize=(1800/100, 400/100), dpi=100)
    plt.xlim(0,18)
    plt.ylim(0,6)
    for i in range(1,7,2):
        for j in range(6):
            k=(i-1)/2
            crate = i % 2
            card = i + (i + 1) % 2 + j // 3
            if j%3==0:
                connector='a'
                channel=1
            elif j%3==1:
                connector='b'
                channel=7
            else:
                connector='c'
                channel=13
            if i==1 and j==2:
                crate==1
                card=9
                connector='b'
                channel=7
            if i==5 and j==2:
                crate==1
                card=9
                connector='c'
                channel=13
            
            sql=f"SELECT hv_voltage_{channel},hv_voltage_{channel+1},hv_voltage_{channel+2},hv_voltage_{channel+3},hv_voltage_{channel+4},hv_voltage_{channel+5},hv_current_{channel},hv_current_{channel+1},hv_current_{channel+2},hv_current_{channel+3},hv_current_{channel+4},hv_current_{channel+5} from tracker_power WHERE crate = {crate} AND card = {card}  order by gcutime desc limit 1;"
            data=conn.root.query(sql)
            HV = loads(data)
            
            color_m0='#FFC0CB'if HV[-1][0]>=200 and HV[-1][6]<=5900 and HV[-1][0]<=1000 else '#CAEBD8'
            color_m1='#FFC0CB'if HV[-1][1]>=200 and HV[-1][7]<=5900 and HV[-1][1]<=1000 else '#CAEBD8'
            color_m2='#FFC0CB'if HV[-1][2]>=200 and HV[-1][8]<=5900 and HV[-1][2]<=1000 else '#CAEBD8'
            color_m3='#FFC0CB'if HV[-1][3]>=200 and HV[-1][9]<=5900 and HV[-1][3]<=1000 else '#CAEBD8'
            color_m4='#FFC0CB'if HV[-1][4]>=200 and HV[-1][10]<=5900 and HV[-1][4]<=1000 else '#CAEBD8'
            color_m5='#FFC0CB'if HV[-1][5]>=200 and HV[-1][11]<=5900 and HV[-1][5]<=1000 else '#CAEBD8'
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [0, 0, 1, 1], color=color_m0)
            plt.text(j+k*6+0.25, 0.70, f'{HV[-1][0]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 0.20, f'{HV[-1][6]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[0,1],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [1, 1, 2, 2], color=color_m1)
            plt.text(j+k*6+0.25, 1.70, f'{HV[-1][1]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 1.20, f'{HV[-1][7]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[1,2],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [2, 2, 3, 3], color=color_m2)
            plt.text(j+k*6+0.25, 2.70, f'{HV[-1][2]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 2.20, f'{HV[-1][8]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[2,3],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [3, 3, 4, 4], color=color_m3)
            plt.text(j+k*6+0.25, 3.70, f'{HV[-1][3]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 3.20, f'{HV[-1][9]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[3,4],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [4, 4, 5, 5], color=color_m4)
            plt.text(j+k*6+0.25, 4.70, f'{HV[-1][4]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 4.20, f'{HV[-1][10]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[4,5],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [5, 5, 6, 6], color=color_m5)
            plt.text(j+k*6+0.25, 5.70, f'{HV[-1][5]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 5.20, f'{HV[-1][11]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[5,6],color='white',linestyle='dashed', linewidth=1)
    
    for i in range(18):
        ax.axvline(x=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(6):
        ax.axhline(y=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(1, 3):
        ax.axvline(x=i * 6, color='black', linestyle='-', linewidth=2)
    plt.grid(True, linestyle='--', linewidth=0.5)
    ax.set_xticks([i +0.5 for i in range(18)], [f'ROW {i //6 *2+1}{i%6}' for i in range(18)])
    ax.set_yticks([i +1/2 for i in range(6)], [f'Mod {i}' for i in range(6)])
    plt.tight_layout()
    plt.savefig('./static/images/power_status_hv_odd.png')   
    plt.close()



def plot_power_hvlv_status():
    fig, ax = plt.subplots(figsize=(1800/100, 600/100), dpi=100)
    conn= rpyc.connect('127.0.0.1', 44555)
    plt.xlim(0,12)
    plt.ylim(0,8)
    for i in range(0,3,2):
        for j in range(6):
            k=i/2
            crate = i % 2
            card = i + (i + 1) % 2 + j // 3
            if j%3==0:
                connector='a'
                channel=1
            elif j%3==1:
                connector='b'
                channel=7
            else:
                connector='c'
                channel=13
            if i==1 and j==2:
                crate==1
                card=9
                connector='b'
                channel=7
            if i==5 and j==2:
                crate==1
                card=9
                connector='c'
                channel=13
            
            sql=f"SELECT hv_voltage_{channel},hv_voltage_{channel+1},hv_voltage_{channel+2},hv_voltage_{channel+3},hv_voltage_{channel+4},hv_voltage_{channel+5},hv_current_{channel},hv_current_{channel+1},hv_current_{channel+2},hv_current_{channel+3},hv_current_{channel+4},hv_current_{channel+5} from tracker_power WHERE crate = {crate} AND card = {card}  order by gcutime desc limit 1;"
            data=conn.root.query(sql)
            HV = loads(data)
            
            color_m0='#FFC0CB' if HV[-1][0]>=200 and HV[-1][6]<=5900 and HV[-1][0]<=1000 else '#CAEBD8'
            color_m1='#FFC0CB'if HV[-1][1]>=200 and HV[-1][7]<=5900 and HV[-1][1]<=1000 else '#CAEBD8'
            color_m2='#FFC0CB'if HV[-1][2]>=200 and HV[-1][8]<=5900 and HV[-1][2]<=1000 else '#CAEBD8'
            color_m3='#FFC0CB'if HV[-1][3]>=200 and HV[-1][9]<=5900 and HV[-1][3]<=1000 else '#CAEBD8'
            color_m4='#FFC0CB'if HV[-1][4]>=200 and HV[-1][10]<=5900 and HV[-1][4]<=1000 else '#CAEBD8'
            color_m5='#FFC0CB'if HV[-1][5]>=200 and HV[-1][11]<=5900 and HV[-1][5]<=1000 else '#CAEBD8'
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [0, 0, 1, 1], color=color_m0)
            ax.text(j+k*6+0.25, 0.70, f'{HV[-1][0]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 0.25, f'{HV[-1][6]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[0,1],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [1, 1, 2, 2], color=color_m1)
            plt.text(j+k*6+0.25, 1.70, f'{HV[-1][1]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 1.25, f'{HV[-1][7]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[1,2],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [2, 2, 3, 3], color=color_m2)
            plt.text(j+k*6+0.25, 2.70, f'{HV[-1][2]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 2.25, f'{HV[-1][8]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[2,3],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [3, 3, 4, 4], color=color_m3)
            plt.text(j+k*6+0.25, 3.70, f'{HV[-1][3]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 3.25, f'{HV[-1][9]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[3,4],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [4, 4, 5, 5], color=color_m4)
            plt.text(j+k*6+0.25, 4.70, f'{HV[-1][4]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 4.25, f'{HV[-1][10]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[4,5],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [5, 5, 6, 6], color=color_m5)
            plt.text(j+k*6+0.25, 5.70, f'{HV[-1][5]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 5.25, f'{HV[-1][11]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[5,6],color='white',linestyle='dashed', linewidth=1)

            sql=f"SELECT lv_d3v8_{connector}, lv_d2v8_{connector}, lv_a2v8_{connector}, lv_a3v3_{connector} ,lv_d3i8_{connector}, lv_d2i8_{connector}, lv_a2i8_{connector}, lv_a3i3_{connector} from tracker_power WHERE crate = {crate} AND card = {card}  order by gcutime desc limit 1;"
            data=conn.root.query(sql)
            LV = loads(data)
        
            color_IF = '#FFC0CB'if LV[-1][0]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_digital = '#FFC0CB'if LV[-1][1]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_analog = '#FFC0CB'if LV[-1][2]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_calibration = '#FFC0CB'if LV[-1][3]>=2000 and LV[-1][6]>100 else '#CAEBD8'
       
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [6, 6, 6.5, 6.5], color=color_IF)
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [6, 6, 6.5, 6.5], color=color_IF)
            plt.text(j+k*6+0.25, 6.25, f'{ LV[-1][0]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.75, 6.25, f'{LV[-1][4]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [6.5,6.5,7,7], color=color_digital)
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [6.5,6.5,7,7], color=color_digital)
            plt.text(j+k*6+0.25, 6.75, f'{ LV[-1][1]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.75, 6.75, f'{LV[-1][5]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [7, 7, 7.5, 7.5], color=color_analog) 
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [7, 7, 7.5, 7.5], color=color_analog) 
            plt.text(j+k*6+0.25, 7.25, f'{ LV[-1][2]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.75, 7.25, f'{LV[-1][6]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [7.5, 7.5, 8, 8], color=color_calibration)
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [7.5, 7.5, 8, 8], color=color_calibration)
            plt.text(j+k*6+0.25, 7.75, f'{ LV[-1][3]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey') 
            plt.text(j+k*6+0.75, 7.75, f'{LV[-1][7]}mA', ha='center', va='center', fontsize=10,color='b')
    
    plt.plot([0,12],[6.5,6.5],color='white',linestyle='dashed', linewidth=1)
    plt.plot([0,12],[7.5,7.5],color='white',linestyle='dashed', linewidth=1)
    plt.plot([0,12],[6,6],color='black',linestyle='-', linewidth=2)
    plt.plot([0,12],[7,7],color='white',linestyle='-', linewidth=1.5)
    for i in range(12):
        plt.plot([i+0.5,i+0.5],[6,8],color='white',linestyle='dashed', linewidth=1)
    for i in range(12):
        ax.axvline(x=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(6):
        ax.axhline(y=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(1, 3):
        ax.axvline(x=i * 6, color='black', linestyle='-', linewidth=2)
    fig.patch.set_alpha(0.) 
    plt.grid(True, linestyle='--', linewidth=0.5)
    ax.set_xticks([i +0.5 for i in range(12)], [f'ROW {i //6 *2}{i%6}' for i in range(12)])
    ax.set_yticks([i+0.5  for i in range(6)]+[i*0.5+6.25 for i in range(4)], [f'Mod {i}' for i in range(6)]+['IF','Digital','Analog','Calibration'])
    plt.tight_layout()
    plt.savefig('./static/images/power_status_hvlv_even_1.png')   
    plt.close()
    
    
    fig, ax = plt.subplots(figsize=(1800/100, 600/100), dpi=100)
    plt.xlim(0,12)
    plt.ylim(0,8)
    for i in range(4,7,2):
        for j in range(6):
            k=(i-4)/2
            crate = i % 2
            card = i + (i + 1) % 2 + j // 3
            if j%3==0:
                connector='a'
                channel=1
            elif j%3==1:
                connector='b'
                channel=7
            else:
                connector='c'
                channel=13
            if i==1 and j==2:
                crate==1
                card=9
                connector='b'
                channel=7
            if i==5 and j==2:
                crate==1
                card=9
                connector='c'
                channel=13
            
            sql=f"SELECT hv_voltage_{channel},hv_voltage_{channel+1},hv_voltage_{channel+2},hv_voltage_{channel+3},hv_voltage_{channel+4},hv_voltage_{channel+5},hv_current_{channel},hv_current_{channel+1},hv_current_{channel+2},hv_current_{channel+3},hv_current_{channel+4},hv_current_{channel+5} from tracker_power WHERE crate = {crate} AND card = {card}  order by gcutime desc limit 1;"
            data=conn.root.query(sql)
            HV = loads(data)
            
            color_m0='#FFC0CB'if HV[-1][0]>=200 and HV[-1][6]<=5900 and HV[-1][0]<=1000 else '#CAEBD8'
            color_m1='#FFC0CB'if HV[-1][1]>=200 and HV[-1][7]<=5900 and HV[-1][1]<=1000 else '#CAEBD8'
            color_m2='#FFC0CB'if HV[-1][2]>=200 and HV[-1][8]<=5900 and HV[-1][2]<=1000 else '#CAEBD8'
            color_m3='#FFC0CB'if HV[-1][3]>=200 and HV[-1][9]<=5900 and HV[-1][3]<=1000 else '#CAEBD8'
            color_m4='#FFC0CB'if HV[-1][4]>=200 and HV[-1][10]<=5900 and HV[-1][4]<=1000 else '#CAEBD8'
            color_m5='#FFC0CB'if HV[-1][5]>=200 and HV[-1][11]<=5900 and HV[-1][5]<=1000 else '#CAEBD8'
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [0, 0, 1, 1], color=color_m0)
            plt.text(j+k*6+0.25, 0.70, f'{HV[-1][0]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 0.25, f'{HV[-1][6]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[0,1],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [1, 1, 2, 2], color=color_m1)
            plt.text(j+k*6+0.25, 1.70, f'{HV[-1][1]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 1.25, f'{HV[-1][7]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[1,2],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [2, 2, 3, 3], color=color_m2)
            plt.text(j+k*6+0.25, 2.70, f'{HV[-1][2]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 2.25, f'{HV[-1][8]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[2,3],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [3, 3, 4, 4], color=color_m3)
            plt.text(j+k*6+0.25, 3.70, f'{HV[-1][3]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 3.25, f'{HV[-1][9]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[3,4],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [4, 4, 5, 5], color=color_m4)
            plt.text(j+k*6+0.25, 4.70, f'{HV[-1][4]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 4.25, f'{HV[-1][10]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[4,5],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [5, 5, 6, 6], color=color_m5)
            plt.text(j+k*6+0.25, 5.70, f'{HV[-1][5]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 5.25, f'{HV[-1][11]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[5,6],color='white',linestyle='dashed', linewidth=1)

            sql=f"SELECT lv_d3v8_{connector}, lv_d2v8_{connector}, lv_a2v8_{connector}, lv_a3v3_{connector} ,lv_d3i8_{connector}, lv_d2i8_{connector}, lv_a2i8_{connector}, lv_a3i3_{connector} from tracker_power WHERE crate = {crate} AND card = {card}  order by gcutime desc limit 1;"
            data=conn.root.query(sql)
            LV = loads(data)
        
            color_IF = '#FFC0CB'if LV[-1][0]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_digital = '#FFC0CB'if LV[-1][1]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_analog = '#FFC0CB'if LV[-1][2]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_calibration = '#FFC0CB'if LV[-1][3]>=2000 and LV[-1][6]>100 else '#CAEBD8'
             
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [6, 6, 6.5, 6.5], color=color_IF)
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [6, 6, 6.5, 6.5], color=color_IF)
            plt.text(j+k*6+0.25, 6.25, f'{ LV[-1][0]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.75, 6.25, f'{LV[-1][4]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [6.5,6.5,7,7], color=color_digital)
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [6.5,6.5,7,7], color=color_digital)
            plt.text(j+k*6+0.25, 6.75, f'{ LV[-1][1]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.75, 6.75, f'{LV[-1][5]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [7, 7, 7.5, 7.5], color=color_analog) 
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [7, 7, 7.5, 7.5], color=color_analog) 
            plt.text(j+k*6+0.25, 7.25, f'{ LV[-1][2]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.75, 7.25, f'{LV[-1][6]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [7.5, 7.5, 8, 8], color=color_calibration)
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [7.5, 7.5, 8, 8], color=color_calibration)
            plt.text(j+k*6+0.25, 7.75, f'{ LV[-1][3]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey') 
            plt.text(j+k*6+0.75, 7.75, f'{LV[-1][7]}mA', ha='center', va='center', fontsize=10,color='b')
    fig.patch.set_alpha(0.) 
    plt.plot([0,12],[6,6],color='black',linestyle='-', linewidth=2)
    plt.plot([0,12],[7,7],color='white',linestyle='-', linewidth=1.5)
    plt.plot([0,12],[6.5,6.5],color='white',linestyle='dashed', linewidth=1)
    plt.plot([0,12],[7.5,7.5],color='white',linestyle='dashed', linewidth=1)
    for i in range(12):
        plt.plot([i+0.5,i+0.5],[6,8],color='white',linestyle='dashed', linewidth=1)
    for i in range(12):
        ax.axvline(x=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(6):
        ax.axhline(y=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(1, 3):
        ax.axvline(x=i * 6, color='black', linestyle='-', linewidth=2)
    plt.grid(True, linestyle='--', linewidth=0.5)
    ax.set_xticks([i +0.5 for i in range(12)], [f'ROW {i //6 *2+4}{i%6}' for i in range(12)])
    ax.set_yticks([i+0.5  for i in range(6)]+[i*0.5+6.25 for i in range(4)], [f'Mod {i}' for i in range(6)]+['IF','Digital','Analog','Calibration'])
    plt.tight_layout()
    plt.savefig('./static/images/power_status_hvlv_even_2.png')   
    plt.close()
    

    fig, ax = plt.subplots(figsize=(1800/100, 600/100), dpi=100)
    plt.xlim(0,12)
    plt.ylim(0,8)
    for i in range(1,5,2):
        for j in range(6):
            k=(i-1)/2
            crate = i % 2
            card = i + (i + 1) % 2 + j // 3
            if j%3==0:
                connector='a'
                channel=1
            elif j%3==1:
                connector='b'
                channel=7
            else:
                connector='c'
                channel=13
            if i==1 and j==2:
                crate==1
                card=9
                connector='b'
                channel=7
            if i==5 and j==2:
                crate==1
                card=9
                connector='c'
                channel=13
            
            sql=f"SELECT hv_voltage_{channel},hv_voltage_{channel+1},hv_voltage_{channel+2},hv_voltage_{channel+3},hv_voltage_{channel+4},hv_voltage_{channel+5},hv_current_{channel},hv_current_{channel+1},hv_current_{channel+2},hv_current_{channel+3},hv_current_{channel+4},hv_current_{channel+5} from tracker_power WHERE crate = {crate} AND card = {card}  order by gcutime desc limit 1;"
            data=conn.root.query(sql)
            HV = loads(data)
          
            color_m0='#FFC0CB'if HV[-1][0]>=200 and HV[-1][6]<=5900 and HV[-1][0]<=1000 else '#CAEBD8'
            color_m1='#FFC0CB'if HV[-1][1]>=200 and HV[-1][7]<=5900 and HV[-1][1]<=1000 else '#CAEBD8'
            color_m2='#FFC0CB'if HV[-1][2]>=200 and HV[-1][8]<=5900 and HV[-1][2]<=1000 else '#CAEBD8'
            color_m3='#FFC0CB'if HV[-1][3]>=200 and HV[-1][9]<=5900 and HV[-1][3]<=1000 else '#CAEBD8'
            color_m4='#FFC0CB'if HV[-1][4]>=200 and HV[-1][10]<=5900 and HV[-1][4]<=1000 else '#CAEBD8'
            color_m5='#FFC0CB'if HV[-1][5]>=200 and HV[-1][11]<=5900 and HV[-1][5]<=1000 else '#CAEBD8'
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [0, 0, 1, 1], color=color_m0)
            plt.text(j+k*6+0.25, 0.70, f'{HV[-1][0]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 0.20, f'{HV[-1][6]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[0,1],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [1, 1, 2, 2], color=color_m1)
            plt.text(j+k*6+0.25, 1.70, f'{HV[-1][1]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 1.20, f'{HV[-1][7]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[1,2],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [2, 2, 3, 3], color=color_m2)
            plt.text(j+k*6+0.25, 2.70, f'{HV[-1][2]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 2.20, f'{HV[-1][8]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[2,3],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [3, 3, 4, 4], color=color_m3)
            plt.text(j+k*6+0.25, 3.70, f'{HV[-1][3]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 3.20, f'{HV[-1][9]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[3,4],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [4, 4, 5, 5], color=color_m4)
            plt.text(j+k*6+0.25, 4.70, f'{HV[-1][4]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 4.20, f'{HV[-1][10]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[4,5],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [5, 5, 6, 6], color=color_m5)
            plt.text(j+k*6+0.25, 5.70, f'{HV[-1][5]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 5.20, f'{HV[-1][11]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[5,6],color='white',linestyle='dashed', linewidth=1)

            sql=f"SELECT lv_d3v8_{connector}, lv_d2v8_{connector}, lv_a2v8_{connector}, lv_a3v3_{connector} ,lv_d3i8_{connector}, lv_d2i8_{connector}, lv_a2i8_{connector}, lv_a3i3_{connector} from tracker_power WHERE crate = {crate} AND card = {card}  order by gcutime desc limit 1;"
            data=conn.root.query(sql)
            LV = loads(data)
        
            color_IF = '#FFC0CB'if LV[-1][0]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_digital = '#FFC0CB'if LV[-1][1]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_analog = '#FFC0CB'if LV[-1][2]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_calibration = '#FFC0CB'if LV[-1][3]>=2000 and LV[-1][6]>100 else '#CAEBD8'
       
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [6, 6, 6.5, 6.5], color=color_IF)
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [6, 6, 6.5, 6.5], color=color_IF)
            plt.text(j+k*6+0.25, 6.25, f'{ LV[-1][0]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.75, 6.25, f'{LV[-1][4]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [6.5,6.5,7,7], color=color_digital)
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [6.5,6.5,7,7], color=color_digital)
            plt.text(j+k*6+0.25, 6.75, f'{ LV[-1][1]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.75, 6.75, f'{LV[-1][5]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [7, 7, 7.5, 7.5], color=color_analog) 
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [7, 7, 7.5, 7.5], color=color_analog) 
            plt.text(j+k*6+0.25, 7.25, f'{ LV[-1][2]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.75, 7.25, f'{LV[-1][6]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [7.5, 7.5, 8, 8], color=color_calibration)
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [7.5, 7.5, 8, 8], color=color_calibration)
            plt.text(j+k*6+0.25, 7.75, f'{ LV[-1][3]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey') 
            plt.text(j+k*6+0.75, 7.75, f'{LV[-1][7]}mA', ha='center', va='center', fontsize=10,color='b')
    fig.patch.set_alpha(0.) 
    plt.plot([0,12],[6,6],color='black',linestyle='-', linewidth=2)
    plt.plot([0,12],[7,7],color='white',linestyle='-', linewidth=1.5)
    plt.plot([0,12],[6.5,6.5],color='white',linestyle='dashed', linewidth=1)
    plt.plot([0,12],[7.5,7.5],color='white',linestyle='dashed', linewidth=1)
    for i in range(12):
        plt.plot([i+0.5,i+0.5],[6,8],color='white',linestyle='dashed', linewidth=1)
    for i in range(12):
        ax.axvline(x=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(6):
        ax.axhline(y=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(1, 2):
        ax.axvline(x=i * 6, color='black', linestyle='-', linewidth=2)
    
    plt.grid(True, linestyle='--', linewidth=0.5)
    ax.set_xticks([i +0.5 for i in range(12)], [f'ROW {i //6 *2+1}{i%6}' for i in range(12)])
    ax.set_yticks([i+0.5  for i in range(6)]+[i*0.5+6.25 for i in range(4)], [f'Mod {i}' for i in range(6)]+['IF','Digital','Analog','Calibration'])
    plt.tight_layout()
    plt.savefig('./static/images/power_status_hvlv_odd1.png')   
    plt.close()

    fig, ax = plt.subplots(figsize=(900/100, 600/100), dpi=100)
    plt.xlim(0,6)
    plt.ylim(0,8)
    for i in range(5,6,1):
        for j in range(6):
            k=(i-5)/2
            crate = i % 2
            card = i + (i + 1) % 2 + j // 3
            if j%3==0:
                connector='a'
                channel=1
            elif j%3==1:
                connector='b'
                channel=7
            else:
                connector='c'
                channel=13
            if i==1 and j==2:
                crate==1
                card=9
                connector='b'
                channel=7
            if i==5 and j==2:
                crate==1
                card=9
                connector='c'
                channel=13
            
            sql=f"SELECT hv_voltage_{channel},hv_voltage_{channel+1},hv_voltage_{channel+2},hv_voltage_{channel+3},hv_voltage_{channel+4},hv_voltage_{channel+5},hv_current_{channel},hv_current_{channel+1},hv_current_{channel+2},hv_current_{channel+3},hv_current_{channel+4},hv_current_{channel+5} from tracker_power WHERE crate = {crate} AND card = {card}  order by gcutime desc limit 1;"
            data=conn.root.query(sql)
            HV = loads(data)
          
            color_m0='#FFC0CB'if HV[-1][0]>=200 and HV[-1][6]<=5900 and HV[-1][0]<=1000 else '#CAEBD8'
            color_m1='#FFC0CB'if HV[-1][1]>=200 and HV[-1][7]<=5900 and HV[-1][1]<=1000 else '#CAEBD8'
            color_m2='#FFC0CB'if HV[-1][2]>=200 and HV[-1][8]<=5900 and HV[-1][2]<=1000 else '#CAEBD8'
            color_m3='#FFC0CB'if HV[-1][3]>=200 and HV[-1][9]<=5900 and HV[-1][3]<=1000 else '#CAEBD8'
            color_m4='#FFC0CB'if HV[-1][4]>=200 and HV[-1][10]<=5900 and HV[-1][4]<=1000 else '#CAEBD8'
            color_m5='#FFC0CB'if HV[-1][5]>=200 and HV[-1][11]<=5900 and HV[-1][5]<=1000 else '#CAEBD8'
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [0, 0, 1, 1], color=color_m0)
            plt.text(j+k*6+0.25, 0.70, f'{HV[-1][0]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 0.20, f'{HV[-1][6]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[0,1],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [1, 1, 2, 2], color=color_m1)
            plt.text(j+k*6+0.25, 1.70, f'{HV[-1][1]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 1.20, f'{HV[-1][7]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[1,2],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [2, 2, 3, 3], color=color_m2)
            plt.text(j+k*6+0.25, 2.70, f'{HV[-1][2]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 2.20, f'{HV[-1][8]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[2,3],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [3, 3, 4, 4], color=color_m3)
            plt.text(j+k*6+0.25, 3.70, f'{HV[-1][3]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 3.20, f'{HV[-1][9]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[3,4],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [4, 4, 5, 5], color=color_m4)
            plt.text(j+k*6+0.25, 4.70, f'{HV[-1][4]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 4.20, f'{HV[-1][10]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[4,5],color='white',linestyle='dashed', linewidth=1)
            plt.fill([j+k*6, j+1+k*6, j+1+k*6, j+k*6], [5, 5, 6, 6], color=color_m5)
            plt.text(j+k*6+0.25, 5.70, f'{HV[-1][5]}V', ha='center', va='center', fontsize=10,color="dimgrey")
            plt.text(j+k*6+0.75, 5.20, f'{HV[-1][11]/1000:.1f}μA', ha='center', va='center', fontsize=10,color='b')
            plt.plot([k*6+j,k*6+j+1],[5,6],color='white',linestyle='dashed', linewidth=1)

            sql=f"SELECT lv_d3v8_{connector}, lv_d2v8_{connector}, lv_a2v8_{connector}, lv_a3v3_{connector} ,lv_d3i8_{connector}, lv_d2i8_{connector}, lv_a2i8_{connector}, lv_a3i3_{connector} from tracker_power WHERE crate = {crate} AND card = {card}  order by gcutime desc limit 1;"
            data=conn.root.query(sql)
            LV = loads(data)
        
            color_IF = '#FFC0CB'if LV[-1][0]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_digital = '#FFC0CB'if LV[-1][1]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_analog = '#FFC0CB'if LV[-1][2]>=2000 and LV[-1][6]>100 else '#CAEBD8'
            color_calibration = '#FFC0CB'if LV[-1][3]>=2000 and LV[-1][6]>100 else '#CAEBD8'
       
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [6, 6, 6.5, 6.5], color=color_IF)
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [6, 6, 6.5, 6.5], color=color_IF)
            plt.text(j+k*6+0.25, 6.25, f'{ LV[-1][0]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.75, 6.25, f'{LV[-1][4]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [6.5,6.5,7,7], color=color_digital)
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [6.5,6.5,7,7], color=color_digital)
            plt.text(j+k*6+0.25, 6.75, f'{ LV[-1][1]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.75, 6.75, f'{LV[-1][5]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [7, 7, 7.5, 7.5], color=color_analog) 
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [7, 7, 7.5, 7.5], color=color_analog) 
            plt.text(j+k*6+0.25, 7.25, f'{ LV[-1][2]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey')
            plt.text(j+k*6+0.75, 7.25, f'{LV[-1][6]}mA', ha='center', va='center', fontsize=10,color='b')
            plt.fill([j+k*6, j+0.5+k*6, j+0.5+k*6, j+k*6], [7.5, 7.5, 8, 8], color=color_calibration)
            plt.fill([j+k*6+0.5, j+1+k*6, j+1+k*6, j+0.5+k*6], [7.5, 7.5, 8, 8], color=color_calibration)
            plt.text(j+k*6+0.25, 7.75, f'{ LV[-1][3]/1000:.1f}V', ha='center', va='center', fontsize=10,color='dimgrey') 
            plt.text(j+k*6+0.75, 7.75, f'{LV[-1][7]}mA', ha='center', va='center', fontsize=10,color='b')
    fig.patch.set_alpha(0.) 
    plt.plot([0,6],[6,6],color='black',linestyle='-', linewidth=2)
    plt.plot([0,6],[7,7],color='white',linestyle='-', linewidth=1.5)
    plt.plot([0,6],[6.5,6.5],color='white',linestyle='dashed', linewidth=1)
    plt.plot([0,6],[7.5,7.5],color='white',linestyle='dashed', linewidth=1)
    for i in range(6):
        plt.plot([i+0.5,i+0.5],[6,8],color='white',linestyle='dashed', linewidth=1)
    for i in range(6):
        ax.axvline(x=i , color='white', linestyle='-', linewidth=1.5)
    for i in range(6):
        ax.axhline(y=i , color='white', linestyle='-', linewidth=1.5)
    
    
    plt.grid(True, linestyle='--', linewidth=0.5)
    ax.set_xticks([i +0.5 for i in range(6)], [f'ROW 5{i%6}' for i in range(6)])
    ax.set_yticks([i+0.5  for i in range(6)]+[i*0.5+6.25 for i in range(4)], [f'Mod {i}' for i in range(6)]+['IF','Digital','Analog','Calibration'])
    plt.tight_layout()
    plt.savefig('./static/images/power_status_hvlv_odd2.png')   
    plt.close()

    