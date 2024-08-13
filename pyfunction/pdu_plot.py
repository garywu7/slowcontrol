import os
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import time 
import datetime
import matplotlib.dates as mdates
import rpyc
from quickle import dumps, loads
from flask import Flask, render_template,request,jsonify
def pdu_power(x):
    return x


def pdu_temp(x):
    voltage = (x * 2.5) / 4096.0
    temp = ((voltage - 0.750) / 0.01) + 25.0
    return temp


def pdu_voltage(x):
    sc = 32.0 / 65536.0
    return x * sc


def pdu_vbat(x):
    sc = (1.0 / 16.0) * (1.0 / 1023.0) * 2.5 * 16
    # 1/16 factor since adc accumulates 16 readings
    # scale by ADC FSR 1023
    # multiply by 2.5 vref
    # factor of 16 from resistive divider

    return x * sc


def pdu_current(x):
    sc = 0.1 / (0.005 * 65536.0)
    return sc * x


def pdu_power_acc(x):
    PwrFSR = 3.2 / 0.005  # 3.2V^2 / 0.01 Ohms = 320 Watts (eq 4-5)
    return (x / 2**28) * (
        PwrFSR / 1024.0
    )  # this is an energy, (Watts / sampling rate)


def asic_temp(x):
    # returns deg C
    #LMT84-Q1
    Gsh = 3.87
    Vt = 900 - (x - 1024) * 1.72 / Gsh #in mV
    return 30 + (5.506 - np.sqrt(math.pow(-5.506,2) + 4*0.00176*(870.6-Vt)))/(2*(-0.00176)) #in C


def asic_leak(x, R):
    return ((1024 - x) * 0.00176) / (5.14 * 10 * R)


def asic_leak_warm(x):
    # returns nA
    return asic_leak(x, 3600) * 1e9


def asic_leak_cold(x):
    # returns nA
    return asic_leak(x, 1950000) * 1e9
def plot_pdu_status(pduid):
    channelname={0:['0:','1: RAT 4,5','2: RAT 18,19','3: Thermal 1','4: Thermal 2','5: RAT 13,14','6:RAT 15,16','7: RAT 2,17'],2:['0:','1:','2: RAT 10,11','3: RAT 12,20','4: RAT 1,3','5: HVLV Odds','6:DAQ 1','7:DAQ 3'],3:['0:TOF Switch','1:TOF sys','2:TIU','3:RAT 8, 9','4:RAT 6,7','5:HVLV Evens','6:DAQ 0','7:DAQ 2']}
    
    fig, ax = plt.subplots(figsize=(1800/100, 400/100), dpi=100)
    
    conn= rpyc.connect('127.0.0.1', 44555)
    plt.xlim(0,8)
    plt.ylim(0,4)
    sql='SELECT '
    for i in range(7):
        sql+=f"vbus_avg{i},vsense_avg{i},vpower_acc{i},temp{i}," 
    sql+=f"vbus_avg7,vsense_avg7,vpower_acc7,temp7 from pdu_hkp where pdu_id={pduid} order by gcutime desc limit 1;"
    data=conn.root.query(sql)
    pdu = loads(data)
    #plt.fill([0, 8, 8, 0], [0, 0, 4, 4], color='#FFC0CB')
    vol=np.array([])
    cur=np.array([])
    for i in range(32):
        channel= i % 8 
        layer = i//8
        if layer == 0:
            vol=np.append(vol,pdu_voltage(pdu[-1][channel*4+layer]))
            ax.text( channel+0.5, 4-(layer+0.5), f'{pdu_voltage(pdu[-1][channel*4+layer]):.2f}', ha='center', va='center', fontsize=10,color='b')
            if pdu_voltage(pdu[-1][channel*4+layer])>10:plt.fill([channel,channel+1,channel+1,channel],[0,0,4,4],color='#FFC0CB')
            else:plt.fill([channel,channel+1,channel+1,channel],[0,0,4,4],color='#CAEBD8')
        elif layer==1:
            cur=np.append(cur,pdu_current(pdu[-1][channel*4+layer]))
            ax.text( channel+0.5, 4-(layer+0.5), f'{pdu_current(pdu[-1][channel*4+layer]):.2f}', ha='center', va='center', fontsize=10,color='b')
        elif layer==2:
            ax.text( channel+0.5, 4-(layer+0.5), f'{cur[channel]*vol[channel]:.2f}', ha='center', va='center', fontsize=10,color='b')
        else:
            ax.text( channel+0.5, 4-(layer+0.5), f'{pdu_temp(pdu[-1][channel*4+layer] ):.2f}', ha='center', va='center', fontsize=10,color='b')
    # 根据开关状态设置方块的颜色，开启为黑色，关闭为白色
        
    for i in range(5):
        ax.axhline(y=i , color='white', linestyle='-', linewidth=1.5)
    
    for i in range(8):
        ax.axvline(x=i , color='white', linestyle='-', linewidth=1.5)
    
    fig.patch.set_alpha(0.) 
    ax.set_xticks([i + 0.5 for i in range(8)], [f'{channelname[pduid][i]}' for i in range(8)], fontsize=14)
   
    ax.set_yticks([i * 1+ 0.5 for i in range(4)], ['Temp [C]','Power Acc [W]','AVE I [A]','Ave Voltage [V]'], fontsize=14)
    ax.set_title(f'PDU {pduid}', fontsize=18)
   
    plt.savefig(f'./static/images/pdu_test_{pduid}.png') 
    plt.close(fig)
def pdu_load(timeperiod,pduid):
    try:
        time_end_string=request.form['timeend']
        dt = datetime.datetime.strptime(time_end_string, "%Y/%m/%d/%H/%M").replace(tzinfo=datetime.timezone.utc)
        timeend=dt.timestamp()
    except:
        timeend = int(time.time())
    try:
        time_begin_string=request.form['timebegin']
        dt = datetime.datetime.strptime(time_begin_string, "%Y/%m/%d/%H/%M").replace(tzinfo=datetime.timezone.utc)
        timebegin=dt.timestamp()
    except:
        timebegin = timeend - int(timeperiod) * 60
    utc_time_begin = datetime.datetime.utcfromtimestamp(timebegin)
    utc_time_end = datetime.datetime.utcfromtimestamp(timeend)
    conn= rpyc.connect('127.0.0.1', 44555)
    cl=['b','g','r','c','m','y','orange','purple']
    sql='SELECT '
    for i in range(7):
        sql+=f"vbus_avg{i},vsense_avg{i},vpower_acc{i},temp{i}," 
    sql+=f"vbus_avg7,vsense_avg7,vpower_acc7,temp7,gcutime from pdu_hkp where pdu_id={pduid} and gcutime<{timeend} and gcutime>{timebegin};"
    data=conn.root.query(sql)
    pdu = loads(data)
    ti_int = [int(ts[-1]) for ts in pdu]
    utc_times = [datetime.datetime.utcfromtimestamp(ts) for ts in ti_int]

    fig, ax = plt.subplots(figsize=(1800/100, 400/100), dpi=100)
    plt.xticks(rotation=45)
    plt.xlabel('Time (UTC)')
    plt.xlim(utc_time_begin,utc_time_end)
    for j in range (8):
        v_ch=[pdu_voltage(ts[4*j])for ts in pdu]
        #lv_digital=[ts[2] for ts in LV]
        #lv_analog=[ts[3] for ts in LV]
        #lv_calib=[ts[4] for ts in LV]           
        plt.plot(utc_times, v_ch,color=cl[j])
    plt.ylabel('Average Voltage(V)')
    plt.tight_layout()
    plt.savefig(f'./static/images/pdu_voltage_pdu{pduid}.png')

    fig, ax = plt.subplots(figsize=(1800/100, 400/100), dpi=100)
    plt.xticks(rotation=45)
    plt.xlabel('Time (UTC)')
    plt.xlim(utc_time_begin,utc_time_end)
    for j in range (8):
        I_ch=[pdu_current(ts[4*j+1])for ts in pdu]
        #lv_digital=[ts[2] for ts in LV]
        #lv_analog=[ts[3] for ts in LV]
        #lv_calib=[ts[4] for ts in LV]           
        plt.plot(utc_times, I_ch,color=cl[j])
    plt.ylabel('Average I (A)')
    plt.tight_layout()
    plt.savefig(f'./static/images/pdu_current_pdu{pduid}.png')

    fig, ax = plt.subplots(figsize=(1800/100, 400/100), dpi=100)
    plt.xticks(rotation=45)
    plt.xlabel('Time (UTC)')
    plt.xlim(utc_time_begin,utc_time_end)
    for j in range (8):
        P_ch=[pdu_current(ts[4*j+1])*pdu_voltage(ts[4*j])for ts in pdu]
        #lv_digital=[ts[2] for ts in LV]
        #lv_analog=[ts[3] for ts in LV]
        #lv_calib=[ts[4] for ts in LV]           
        plt.plot(utc_times, P_ch,color=cl[j])
    plt.ylabel('Power Acc(W)')
    plt.tight_layout()
    plt.savefig(f'./static/images/pdu_power_pdu{pduid}.png')

    fig, ax = plt.subplots(figsize=(1800/100, 400/100), dpi=100)
    plt.xticks(rotation=45)
    plt.xlabel('Time (UTC)')
    plt.xlim(utc_time_begin,utc_time_end)
    for j in range (8):
        t_ch=[pdu_temp(ts[4*j+3]) for ts in pdu]
        #lv_digital=[ts[2] for ts in LV]
        #lv_analog=[ts[3] for ts in LV]
        #lv_calib=[ts[4] for ts in LV]           
        plt.plot(utc_times, t_ch,color=cl[j])
    plt.ylabel('Temp(C)')
    plt.tight_layout()
    plt.savefig(f'./static/images/pdu_temp_pdu{pduid}.png')

   
    