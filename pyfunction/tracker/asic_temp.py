import os
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template,request,jsonify
import time 
import datetime
import matplotlib.dates as mdates
from math import sqrt
import rpyc
from quickle import dumps, loads
def temp_trans(adc_code):
    V_T=900-(adc_code-1024)*1.76/3.87
    T=30+(5.506-sqrt(5.506*5.506+4*0.00176*(870.6-V_T)))/(2*-0.00176)
    return T 
def temp_heat(layer):
    cl=['b','g','r','c','m','y']
    
    conn= rpyc.connect('127.0.0.1', 44555)
    #conn = sqlite3.connect('gsedb_nts.sqlite')
    #cursor = conn.cursor()
    temp_adc = {}
    fig, ax = plt.subplots(figsize=(6, 5))
    
    temp=np.zeros((6, 6), dtype=float)
    sql=f'SELECT templeak_r0m0,templeak_r0m1,templeak_r0m2,templeak_r0m3,templeak_r0m4,templeak_r0m5,templeak_r1m0,templeak_r1m1,templeak_r1m2,templeak_r1m3,templeak_r1m4,templeak_r1m5,templeak_r2m0,templeak_r2m1,templeak_r2m2,templeak_r2m3,templeak_r2m4,templeak_r2m5,templeak_r3m0,templeak_r3m1,templeak_r3m2,templeak_r3m3,templeak_r3m4,templeak_r3m5,templeak_r4m0,templeak_r4m1,templeak_r4m2,templeak_r4m3,templeak_r4m4,templeak_r4m5,templeak_r5m0,templeak_r5m1,templeak_r5m2,templeak_r5m3,templeak_r5m4,templeak_r5m5 FROM gfptrackertempleak WHERE sysid -128== {layer} order by gcutime desc limit 1;'
    data=conn.root.query(sql)
    temp_adc=loads(data)
    if data:
        for i in range(6):
            for j in range(6):
                temp[i,j]=temp_trans(temp_adc[-1][i*6+j])
    else:
        for i in range(6):
            for j in range(6):
                temp[i,j]=0
    
    
    
    # 绘制热图
    cax = ax.matshow(temp, cmap='coolwarm', origin='lower')
    
    # 添加颜色条
    fig.patch.set_alpha(0.) 
    fig.colorbar(cax)
    plt.xlabel('Module',position=(0,-0.2))
    plt.ylabel('Row')
    plt.title(f'Heat Map_L{layer}')
    plt.xticks(np.arange(6), ['0', '1', '2', '3', '4', '5'],position=(0,-0.1))
    # 在每个格子内显示温度数值
    for i in range(6):
        for j in range(6):
            text_to_display = f"{temp[i, j]:.2f}"
            ax.text(j, i, text_to_display, va='center', ha='center', color='black')
    ax.xaxis.set_label_coords(0.55, -0.1)
    plt.tight_layout() 
    plt.savefig(f'./static/images/temp_heatmap_layer{layer}.png')

def plot_asic_temp(layer,timeperiod,row,module):
    
    try:
        time_end_string=request.form['timeend']
        dt = datetime.datetime.strptime(time_end_string, "%Y/%m/%d/%H/%M").replace(tzinfo=datetime.timezone.utc)
        timeend=dt.timestamp()
    except:
        timeend = int(time.time())
        #timeend=1687219200
    try:
        time_begin_string=request.form['timebegin']
        dt = datetime.datetime.strptime(time_begin_string, "%Y/%m/%d/%H/%M").replace(tzinfo=datetime.timezone.utc)
        timebegin=dt.timestamp()
    except:
        timebegin = timeend - int(timeperiod) * 60

    # Convert timestamps to datetime objects
    utc_time_begin = datetime.datetime.utcfromtimestamp(timebegin)
    utc_time_end = datetime.datetime.utcfromtimestamp(timeend)
    cl=['b','g','r','c','m','y']
    #conn = sqlite3.connect('gsedb_nts.sqlite')
    conn= rpyc.connect('127.0.0.1', 44555)

    #cursor = conn.cursor()
    #cursor.execute('SELECT gcutime FROM gfptrackertempleak WHERE gcutime >= ? AND gcutime <= ? AND sysid == ?;',(timebegin,timeend,layer+128,))
    #ti = cursor.fetchall()
    sql=f'SELECT gcutime FROM gfptrackertempleak WHERE gcutime >= {timebegin} AND gcutime <= {timeend} AND sysid-128 == {layer};'
    data=conn.root.query(sql)
    ti=loads(data)
    temp_adc = {}
    temp={}
    if module=='all':
        for i in range(6):
            query=f'SELECT templeak_r{row}m{i} FROM gfptrackertempleak WHERE gcutime >= {timebegin} AND gcutime <= {timeend} AND sysid-128 == {layer};'
            #cursor.execute(query,(timebegin,timeend,layer+128))
            data=conn.root.query(query)
            #temp_adc[f"temp_adc_{i}"]= cursor.fetchall()
            temp_adc[f"temp_adc_{i}"]=loads(data)
        #cursor.close()
        conn.close()
        for i in range(6):
            temp[f"temp_{i}"]=[temp_trans(ts[0])for ts in temp_adc[f"temp_adc_{i}"]]
        ti_int = [int(ts[0]) for ts in ti]
        utc_times = [datetime.datetime.utcfromtimestamp(ts) for ts in ti_int]
        # Plotting
        
        fig, ax = plt.subplots()
        plt.figure(figsize=(1000/100, 500/100), dpi=100)
        #plt.plot(utc_times, temp,marker='o')
        for i in range(6):
            plt.plot(utc_times, temp[f"temp_{i}"],color=cl[i])
        plt.xlim(utc_time_begin,utc_time_end)
        
        # Set x-axis major locator and formatter dynamically
        
        # Format the x-axis ticks as hour:minute
        #ax.set_xticks(hour_ticks)
        #ax.set_xticklabels([h.strftime('%H:%M') for h in hour_ticks])
        
        #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.xticks(rotation=45)
        plt.xlabel('Time (UTC)')
        plt.ylabel('Temperature')
        plt.title(f'Temperature_L{layer}R{row} ')

        plt.tight_layout()
        plt.savefig(f'./static/images/temp_layer{layer}.png')
    else:
        query=f'SELECT templeak_r{row}m{module} FROM gfptrackertempleak WHERE gcutime >= {timebegin} AND gcutime <= {timeend} AND sysid-128 == {layer};'
        #cursor.execute(query)
        data=conn.root.query(query)
        #temp_adc= cursor.fetchall()
        temp_adc=loads(data)
        cursor.close()
        conn.close()
        temp=[temp_trans(ts[0])for ts in temp_adc]
        ti_int = [int(ts[0]) for ts in ti]
        utc_times = [datetime.datetime.utcfromtimestamp(ts) for ts in ti_int]
        # Plotting
        
        fig, ax = plt.subplots()
        plt.figure(figsize=(2000/100, 600/100), dpi=100)
        plt.plot(utc_times, temp,color=cl[i])
        plt.xlim(utc_time_begin,utc_time_end)
        
        # Set x-axis major locator and formatter dynamically
        
        # Format the x-axis ticks as hour:minute
        #ax.set_xticks(hour_ticks)
        #ax.set_xticklabels([h.strftime('%H:%M') for h in hour_ticks])
        
        #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.xticks(rotation=45)
        plt.xlabel('Time (UTC)')
        plt.ylabel('Temperature')
        plt.title(f'Temperature_L{layer}R{row}M{module}')

        plt.tight_layout()
        plt.savefig(f'./static/images/temp_layer{layer}.png')